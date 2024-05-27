from django.db import models
from django.conf import settings

# Create your models here.

class PlayVideo(models.Model):
    video_url = models.URLField()
    
class ClearValue(models.Model):
    game = models.CharField(max_length=500)
    value = models.IntegerField()
    
class Script(models.Model):
    text = models.TextField()
    timing = models.IntegerField()
    
class OurFeedback(models.Model):
    advice = models.TextField()
    is_expert = models.BooleanField()
    is_timely = models.BooleanField
    
class PlayerFeedback(models.Model):
    advice = models.TextField()
    is_expert = models.BooleanField()
    is_timely = models.BooleanField