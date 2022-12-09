from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from kwizzedapi.models.player_response import PlayerResponse
from kwizzedapi.models.answer import Answer

class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_image_url = models.CharField(max_length=200)
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    
    @property
    def response_count(self):
        player_responses = PlayerResponse.objects.filter(player_id=self.id)
        return player_responses.count()
    
    
    @property
    def correct_response_count(self):
        player_responses = PlayerResponse.objects.filter(player_id=self.id)
        correct_answers = player_responses.filter(answer__is_correct=True)
        return correct_answers.count()
    