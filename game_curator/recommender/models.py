from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    # Make user field nullable initially to allow for migration
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    game_id = models.IntegerField()
    name = models.CharField(max_length=255)
    cover_url = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    first_release_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s favorite: {self.name}"
        return f"Favorite: {self.name}"

    class Meta:
        unique_together = ['user', 'game_id']
