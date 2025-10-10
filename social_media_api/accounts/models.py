from django.db import models
from django.contrib.auth.models import AbstractUser

# Create a custom user model that extends Django’s AbstractUser, adding fields such as bio, profile_picture, and followers (a ManyToMany field referencing itself, symmetrical=False).
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.username
