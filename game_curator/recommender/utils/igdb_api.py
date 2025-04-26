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
        f'game_modes.name,themes.name,total_rating,total_rating_count,websites.url,websites.category;'
        f'limit 1;'
    )
    
    game_details = client.make_request("games", details_query)
    
    if not game_details or len(game_details) == 0:
        return None
        
    game = game_details[0]
    
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
    
    return game