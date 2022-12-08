from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from kwizzedapi.models.player_response import PlayerResponse

class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200)
    profile_image_url = models.CharField(max_length=200)
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def token_number(self):
        token = Token.objects.get(user_id=self.user.id)
        return f'{token}'
    
    @property
    def response_count(self):
        player_responses = PlayerResponse.objects.filter(player_id=self.id)
        return player_responses.count()
    
    @property
    def correct_response_count(self):
        player_responses = PlayerResponse.objects.filter(player_id=self.id)
        correct_responses = player_responses.filter(is_correct=True)
        return correct_responses.count()
    