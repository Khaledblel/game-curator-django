from django.db import models

class Favorite(models.Model):
    """Model to store favorited games"""
    game_id = models.IntegerField()
    name = models.CharField(max_length=255)
    cover_url = models.URLField(max_length=500, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    first_release_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
