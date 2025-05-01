from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .utils.gemini_api import get_game_recommendations
from .utils.igdb_api import get_game_details
from .models import Favorite

def landing_page(request):
    """View for the landing page of the game recommender application."""
    return render(request, 'recommender/landing.html')

@login_required
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

@login_required
def toggle_favorite(request):
    """Toggle a game as favorite"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_id = data.get('game_id')
            
            # Check if this game is already favorited
            existing_favorite = Favorite.objects.filter(user=request.user, game_id=game_id).first()
            
            if existing_favorite:
                # Remove from favorites
                existing_favorite.delete()
                return JsonResponse({'success': True, 'added': False})
            else:
                # Add to favorites
                name = data.get('name', '')
                cover_url = data.get('cover_url')
                summary = data.get('summary')
                rating = data.get('rating')
                first_release_date = data.get('first_release_date')
                
                # Convert timestamp to datetime if provided
                release_date = None
                if first_release_date:
                    try:
                        release_date = datetime.fromtimestamp(first_release_date)
                    except:
                        pass
                
                # Create new favorite
                Favorite.objects.create(
                    user=request.user,
                    game_id=game_id,
                    name=name,
                    cover_url=cover_url,
                    summary=summary,
                    rating=rating,
                    first_release_date=release_date
                )
                return JsonResponse({'success': True, 'added': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def get_favorites(request):
    """Get the status of whether a specific game is favorited"""
    if request.method == 'GET':
        game_id = request.GET.get('game_id')
        
        if game_id:
            is_favorite = Favorite.objects.filter(user=request.user, game_id=game_id).exists()
            return JsonResponse({'is_favorite': is_favorite})
        
    return JsonResponse({'is_favorite': False})

@login_required
def favorites_page(request):
    """View for the favorites page"""
    favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'recommender/favorites.html', {'favorites': favorites})