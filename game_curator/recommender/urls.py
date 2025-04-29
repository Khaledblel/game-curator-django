from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('recommend/', views.recommender, name='recommender'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('api/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('api/get-favorites/', views.get_favorites, name='get_favorites'),
]