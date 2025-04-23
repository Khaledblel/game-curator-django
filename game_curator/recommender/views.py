from django.shortcuts import render

def landing_page(request):
    """View for the landing page of the game recommender application."""
    return render(request, 'recommender/landing.html')

def recommender(request):
    """View for the game recommendation form and results."""
    # This will be implemented in future steps
    return render(request, 'recommender/recommender.html')