import os
import requests
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class IGDBClient:
    """Client for interacting with the IGDB API"""
    
    def __init__(self):
        self.client_id = os.getenv('IGDB_CLIENT_ID')
        self.client_secret = os.getenv('IGDB_CLIENT_SECRET')
        self.access_token = None
        self.token_expiry = None
        self.base_url = "https://api.igdb.com/v4"
        
    def _get_access_token(self):
        """Get a new access token from Twitch"""
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        response = requests.post(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access_token"]
            # Set token expiry time (subtract 1 hour for safety margin)
            self.token_expiry = datetime.now() + timedelta(seconds=data["expires_in"] - 3600)
            return True
        else:
            print(f"Failed to get access token: {response.status_code} - {response.text}")
            return False
    
    def _ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if not self.access_token or not self.token_expiry or datetime.now() >= self.token_expiry:
            return self._get_access_token()
        return True
    
    def make_request(self, endpoint, query):
        """Make a request to the IGDB API"""
        if not self._ensure_valid_token():
            return None
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.post(url, headers=headers, data=query)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"IGDB API request failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error making IGDB API request: {e}")
            return None

def get_game_details(game_names):
    """
    Get detailed information about games from IGDB API
    
    Args:
        game_names (list): List of game names to search for
        
    Returns:
        dict: Dictionary containing main game and similar games details
    """
    client = IGDBClient()
    
    if not game_names or len(game_names) == 0:
        return {"main_game": None, "similar_games": []}
    
    main_game_name = game_names[0]
    similar_game_names = game_names[1:] if len(game_names) > 1 else []
    
    # Get detailed information for the main game
    main_game = _search_and_get_game_details(client, main_game_name)
    
    # Get detailed information for similar games
    similar_games = []
    for game_name in similar_game_names:
        game = _search_and_get_game_details(client, game_name)
        if game:
            similar_games.append(game)
    
    return {
        "main_game": main_game,
        "similar_games": similar_games
    }

def _search_and_get_game_details(client, game_name):
    """
    Search for a game by name and get its detailed information
    
    Args:
        client (IGDBClient): IGDB API client
        game_name (str): Name of the game to search for
        
    Returns:
        dict: Detailed game information or None if not found
    """
    # First, search for the game to get its ID
    search_query = f'search "{game_name}"; fields name,id; limit 1;'
    search_results = client.make_request("games", search_query)
    
    if not search_results or len(search_results) == 0:
        return None
    
    game_id = search_results[0]['id']
    
    # Get detailed information for the game with a focused set of fields
    details_query = (
        f'where id = {game_id}; fields name,summary,storyline,first_release_date,rating,'
        f'cover.url,screenshots.url,genres.name,platforms.name,involved_companies.company.name,'
        f'involved_companies.developer,involved_companies.publisher,'
        f'game_modes.name,themes.name,total_rating,total_rating_count,websites.url,websites.category,'
        f'alternative_names.name,dlcs,expansions,franchise,franchises,age_ratings.rating,age_ratings.category,'
        f'language_supports.language.name,language_supports.language.native_name,language_supports.language_support_type.name;'
        f'limit 1;'
    )
    
    game_details = client.make_request("games", details_query)
    
    if not game_details or len(game_details) == 0:
        return None
        
    game = game_details[0]
    
    # Get time-to-beat data
    time_to_beat = _get_time_to_beat(client, game_id)
    if time_to_beat:
        game['time_to_beat'] = time_to_beat
    
    # Process image URLs to ensure they're complete
    if 'cover' in game and 'url' in game['cover']:
        # Replace t_thumb with t_cover_big for higher resolution
        game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_cover_big')
        # Ensure URL starts with https:
        if not game['cover']['url'].startswith('https:'):
            game['cover']['url'] = 'https:' + game['cover']['url']
    
    # Process screenshot URLs similarly
    if 'screenshots' in game:
        for screenshot in game['screenshots']:
            if 'url' in screenshot:
                screenshot['url'] = screenshot['url'].replace('t_thumb', 't_screenshot_big')
                if not screenshot['url'].startswith('https:'):
                    screenshot['url'] = 'https:' + screenshot['url']
    
    # Extract developers and publishers
    developers = []
    publishers = []
    if 'involved_companies' in game:
        for company in game['involved_companies']:
            if 'company' in company and 'name' in company['company']:
                if company.get('developer', False):
                    developers.append(company['company']['name'])
                if company.get('publisher', False):
                    publishers.append(company['company']['name'])
    
    game['developers'] = developers
    game['publishers'] = publishers
    
    # Extract game modes
    game_modes = []
    if 'game_modes' in game:
        for mode in game['game_modes']:
            if 'name' in mode:
                game_modes.append(mode['name'])
    game['game_mode_names'] = game_modes
    
    # Extract themes
    themes = []
    if 'themes' in game:
        for theme in game['themes']:
            if 'name' in theme:
                themes.append(theme['name'])
    game['theme_names'] = themes
    
    # Extract genre names for easier access
    genre_names = []
    if 'genres' in game:
        for genre in game['genres']:
            if 'name' in genre:
                genre_names.append(genre['name'])
    game['genre_names'] = genre_names
    
    # Extract platform names for easier access
    platform_names = []
    if 'platforms' in game:
        for platform in game['platforms']:
            if 'name' in platform:
                platform_names.append(platform['name'])
    game['platform_names'] = platform_names
    
    # Format release date
    if 'first_release_date' in game:
        # IGDB stores dates as UNIX timestamps
        release_date = datetime.fromtimestamp(game['first_release_date'])
        game['release_year'] = release_date.year
        game['formatted_release_date'] = release_date.strftime('%B %d, %Y')
    
    # Find official website and store URLs
    official_website = None
    stores = []
    if 'websites' in game:
        for website in game['websites']:
            # Website categories: 1=official, 2=wikia, 3=wikipedia, 4=facebook, 5=twitter, 6=twitch, 8=instagram, 9=youtube, 10=iphone, 11=ipad, 12=android, 13=steam, 14=reddit, etc.
            if website.get('category') == 1 and 'url' in website:
                official_website = website['url']
            # Store websites
            if website.get('category') in [13, 15, 16, 17] and 'url' in website:  # 13=steam, 15=itch, 16=epicgames, 17=gog
                stores.append(website['url'])
    
    game['official_website'] = official_website
    game['stores'] = stores
    
    # Extract alternative names
    alt_names = []
    if 'alternative_names' in game:
        for alt_name in game['alternative_names']:
            if 'name' in alt_name:
                alt_names.append(alt_name['name'])
    game['alt_names'] = alt_names
    
    # Process age ratings
    # IGDB categories: 1=ESRB, 2=PEGI
    # IGDB ESRB ratings: 6=RP, 7=EC, 8=E, 9=E10+, 10=T, 11=M, 12=AO
    # IGDB PEGI ratings: 1=3, 2=7, 3=12, 4=16, 5=18
    esrb_rating = None
    pegi_rating = None
    
    if 'age_ratings' in game:
        for rating in game['age_ratings']:
            if rating.get('category') == 1:  # ESRB
                esrb_rating = get_esrb_rating_url(rating.get('rating'))
            elif rating.get('category') == 2:  # PEGI
                pegi_rating = get_pegi_rating_url(rating.get('rating'))
    
    game['esrb_rating_cover_url'] = esrb_rating
    game['pegi_rating_cover_url'] = pegi_rating
    
    # Process language support data
    language_support = {}
    if 'language_supports' in game:
        for lang_support in game['language_supports']:
            if ('language' in lang_support and 'language_support_type' in lang_support and
                'name' in lang_support['language'] and 'name' in lang_support['language_support_type']):
                
                support_type = lang_support['language_support_type']['name']
                lang_name = lang_support['language']['name']
                native_name = lang_support['language'].get('native_name', '')
                
                # Group by support type
                if support_type not in language_support:
                    language_support[support_type] = []
                
                language_info = {
                    'name': lang_name,
                    'native_name': native_name
                }
                language_support[support_type].append(language_info)
    
    game['language_support'] = language_support
    
    # Process DLCs and expansions if available
    add_on_ids = []
    if 'dlcs' in game and game['dlcs']:
        add_on_ids.extend(game['dlcs'])
    if 'expansions' in game and game['expansions']:
        add_on_ids.extend(game['expansions'])
        
    if add_on_ids:
        game['add_on_details'] = _get_add_on_details(client, add_on_ids)
    else:
        game['add_on_details'] = []
    
    # Process franchise data if available
    franchise_id = None
    if 'franchise' in game and game['franchise']:
        franchise_id = game['franchise']
    elif 'franchises' in game and game['franchises']:
        franchise_id = game['franchises'][0]
    
    if franchise_id:
        game['franchise_details'] = _get_franchise_details(client, franchise_id)
    else:
        game['franchise_details'] = None
    
    return game

def _get_time_to_beat(client, game_id):
    """
    Get time-to-beat data for a game
    
    Args:
        client (IGDBClient): IGDB API client
        game_id (int): ID of the game
        
    Returns:
        dict: Time-to-beat data or None if not available
    """
    query = f'where game_id = {game_id}; fields hastily, normally, completely, count; limit 1;'
    time_to_beat_data = client.make_request("game_time_to_beats", query)
    
    if not time_to_beat_data or len(time_to_beat_data) == 0:
        return None
    
    result = time_to_beat_data[0]
    
    # Format times for display
    if 'hastily' in result:
        result['hastily_formatted'] = format_playtime(result['hastily'])
    if 'normally' in result:
        result['normally_formatted'] = format_playtime(result['normally'])
    if 'completely' in result:
        result['completely_formatted'] = format_playtime(result['completely'])
        
    return result

def get_esrb_rating_url(rating):
    """
    Map ESRB rating ID to its cover image URL
    
    Args:
        rating (int): ESRB rating ID from IGDB
        
    Returns:
        str: URL to the ESRB rating cover image
    """
    esrb_map = {
        6: "https://www.esrb.org/wp-content/uploads/2019/05/RP.svg",  # Rating Pending
        7: "https://www.esrb.org/wp-content/uploads/2019/05/EC.svg",  # Early Childhood
        8: "https://www.esrb.org/wp-content/uploads/2019/05/E.svg",   # Everyone
        9: "https://www.esrb.org/wp-content/uploads/2019/05/E10plus.svg",  # Everyone 10+
        10: "https://www.esrb.org/wp-content/uploads/2019/05/T.svg",  # Teen
        11: "https://www.esrb.org/wp-content/uploads/2019/05/M.svg",  # Mature
        12: "https://www.esrb.org/wp-content/uploads/2019/05/AO.svg"  # Adults Only
    }
    
    return esrb_map.get(rating)

def get_pegi_rating_url(rating):
    """
    Map PEGI rating ID to its cover image URL
    
    Args:
        rating (int): PEGI rating ID from IGDB
        
    Returns:
        str: URL to the PEGI rating cover image
    """
    pegi_map = {
        1: "https://rating.pegi.info/assets/images/games/age_threshold_icons/3.png",  # PEGI 3
        2: "https://rating.pegi.info/assets/images/games/age_threshold_icons/7.png",  # PEGI 7
        3: "https://rating.pegi.info/assets/images/games/age_threshold_icons/12.png",  # PEGI 12
        4: "https://rating.pegi.info/assets/images/games/age_threshold_icons/16.png",  # PEGI 16
        5: "https://rating.pegi.info/assets/images/games/age_threshold_icons/18.png"   # PEGI 18
    }
    
    return pegi_map.get(rating)

def _get_add_on_details(client, add_on_ids):
    """
    Get details for DLCs and expansions from their IDs
    
    Args:
        client (IGDBClient): IGDB API client
        add_on_ids (list): List of DLC and expansion IDs
        
    Returns:
        list: Detailed add-on information
    """
    if not add_on_ids or len(add_on_ids) == 0:
        return []
    
    # Limit to 15 add-ons to avoid large requests
    add_on_ids = add_on_ids[:15]
    
    # Create a comma-separated list of IDs
    ids_string = ','.join(str(id) for id in add_on_ids)
    
    # Get add-on details
    add_on_query = (
        f'where id = ({ids_string}); '
        f'fields name,summary,cover.url,first_release_date,websites.url,websites.category,category; '
    )
    
    add_on_details = client.make_request("games", add_on_query)
    
    if not add_on_details:
        return []
    
    # Process add-on information
    for add_on in add_on_details:
        # Determine if it's DLC or expansion
        # IGDB category: 0=main_game, 1=dlc_addon, 2=expansion, 3=bundle, 4=standalone_expansion
        if 'category' in add_on:
            if add_on['category'] == 2 or add_on['category'] == 4:
                add_on['type'] = 'Expansion'
            else:
                add_on['type'] = 'DLC'
        else:
            add_on['type'] = 'Add-on'
            
        # Process cover URL
        if 'cover' in add_on and 'url' in add_on['cover']:
            add_on['cover']['url'] = add_on['cover']['url'].replace('t_thumb', 't_cover_big')
            if not add_on['cover']['url'].startswith('https:'):
                add_on['cover']['url'] = 'https:' + add_on['cover']['url']
                
        # Format release date
        if 'first_release_date' in add_on:
            release_date = datetime.fromtimestamp(add_on['first_release_date'])
            add_on['release_year'] = release_date.year
            add_on['formatted_release_date'] = release_date.strftime('%B %d, %Y')
                
        # Find store URLs
        stores = []
        if 'websites' in add_on:
            for website in add_on['websites']:
                if website.get('category') in [13, 15, 16, 17] and 'url' in website:
                    stores.append(website['url'])
        add_on['stores'] = stores
    
    return add_on_details

def _get_franchise_details(client, franchise_id):
    """
    Get detailed information about a franchise and its games
    
    Args:
        client (IGDBClient): IGDB API client
        franchise_id (int): ID of the franchise
        
    Returns:
        dict: Detailed franchise information including games
    """
    # First get the franchise details
    franchise_query = f'where id = {franchise_id}; fields name,slug,url,games;'
    franchise_results = client.make_request("franchises", franchise_query)
    
    if not franchise_results or len(franchise_results) == 0:
        return None
        
    franchise = franchise_results[0]
    
    # Get information about the games in this franchise
    if 'games' in franchise and franchise['games']:
        # Limit to 20 games to avoid large requests
        game_ids = franchise['games'][:20]
        ids_string = ','.join(str(id) for id in game_ids)
        
        # Use version_parent = null to exclude editions of games
        games_query = (
            f'where id = ({ids_string}) & category = 0 & version_parent = null; ' 
            f'fields name,cover.url,first_release_date,rating,total_rating,category; '
            f'sort first_release_date asc;'
        )
        
        franchise_games = client.make_request("games", games_query)
        
        if franchise_games:
            # Process each game
            for game in franchise_games:
                # Process cover URL
                if 'cover' in game and 'url' in game['cover']:
                    game['cover']['url'] = game['cover']['url'].replace('t_thumb', 't_cover_big')
                    if not game['cover']['url'].startswith('https:'):
                        game['cover']['url'] = 'https:' + game['cover']['url']
                    
                # Format release date
                if 'first_release_date' in game:
                    release_date = datetime.fromtimestamp(game['first_release_date'])
                    game['release_year'] = release_date.year
                    game['formatted_release_date'] = release_date.strftime('%B %d, %Y')
                
                # Set game type to Main Game
                game['type'] = 'Main Game'
            
            # Sort by release date (just to make sure)
            franchise_games.sort(key=lambda x: x.get('first_release_date', 0))
            
            franchise['games_details'] = franchise_games
        else:
            franchise['games_details'] = []
    else:
        franchise['games_details'] = []
    
    return franchise

def format_playtime(seconds):
    """
    Format seconds into a readable playtime string (hours and minutes)
    
    Args:
        seconds (int): Time in seconds
        
    Returns:
        str: Formatted time string (e.g., "15h 30m" or "45m")
    """
    if not seconds:
        return None
        
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"