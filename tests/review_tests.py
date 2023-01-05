import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token


class ReviewTests(APITestCase):
        
        fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens', 'reviews']
        
        def setUp(self):
            self.player = Player.objects.first()
            token = Token.objects.get(user=self.player.user)
            self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    
        def test_get_reviews(self):
            """
            Ensure we can get all review objects.
            """
            url = '/reviews'
            response = self.client.get(url)
    
            json_response = json.loads(response.content)
    
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(json_response), 2)
            
        def test_delete_review(self):
            """
            Ensure we can delete a review object.
            """
            url = '/reviews/1'
            response = self.client.delete(url)
    
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)