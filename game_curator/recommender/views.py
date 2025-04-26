from django.shortcuts import render
from django.http import JsonResponse
import json
from .utils.gemini_api import get_game_recommendations
from .utils.igdb_api import get_game_details

def landing_page(request):
    """View for the landing page of the game recommender application."""
    return render(request, 'recommender/landing.html')

def recommender(request):
    """View for the game recommendation form and results."""
    context = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_prompt = data.get('prompt', '')
            
            if user_prompt:
                # Step 1: Get game name recommendations from Gemini API
                game_names = get_game_recommendations(user_prompt)
                
                # Step 2: Get detailed game information from IGDB API
                game_details = get_game_details(game_names)
                
                return JsonResponse({
                    'success': True, 
                    'main_game': game_details['main_game'],
                    'similar_games': game_details['similar_games']
                })
            else:
                return JsonResponse({'success': False, 'error': 'No prompt provided'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # For GET requests, just render the form
    return render(request, 'recommender/recommender.html', context)