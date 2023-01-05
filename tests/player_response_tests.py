import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token



class PlayerResponseTests(APITestCase):
    
    fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens']
    
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_player_response(self):
        """
        Ensure we can create a new player response object.
        """
        url = '/playerresponses'
        data = {
            "playerId": 1,
            "answerId": 1
        }
        response = self.client.post(url, data, format='json')
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["answer"], {"id": 1, "answer_text": "Apollo 11", "question": {'category': 1, 'question_text': 'Which Apollo mission was the first one to land on the Moon?'}, "is_correct": True})
        
    def test_get_player_response(self):
        """
        Ensure we can get a player response object.
        """
        url = '/playerresponses/1'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["player"], 1)
        self.assertEqual(json_response["answer"], {"id": 1, "answer_text": "Apollo 11", "question": {'category': 1, 'question_text': 'Which Apollo mission was the first one to land on the Moon?'}, "is_correct": True})
        
    def test_get_player_responses(self):
        """
        Ensure we can get all player response objects.
        """
        url = '/playerresponses'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 10)
        