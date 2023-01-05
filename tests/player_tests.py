import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token


class PlayerTests(APITestCase):
    
    fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens']
    
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_player(self):
        """
        Ensure we can get a player object.
        """
        url = '/players/8'
        response = self.client.get(url)

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["full_name"], "Steve Brownlee")
        self.assertEqual(json_response["user"]["email"], "steve@steve.steve")
        self.assertEqual(json_response["user"]["username"], "coachsteve")
        self.assertEqual(json_response["user"]["is_staff"], False)
        self.assertEqual(json_response["user"]["is_active"], True)
        self.assertEqual(json_response["bio"], "Head Coach")
        self.assertEqual(json_response["profile_image_url"], "asdfadsf")
        self.assertEqual(json_response["response_count"], 0)
        self.assertEqual(json_response["correct_response_count"], 0)
        
    def test_get_players(self):
        """
        Ensure we can get all player objects.
        """
        url = '/players'
        response = self.client.get(url)

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 11)
    
    
    def test_update_player(self):
        """
        Ensure we can update a player object.
        """
        url = '/players/8'
        data = {
            "username": "CoachSteve58",
            "bio": "Head Coach and lover of sunsets",
            "profileImageUrl": "asdfadsfdasdf",
            "isActive": True,
            "email": "steviewonder@gmail.com",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        json_response = json.loads(response.content)

        # assert the the updated values are correct
        
        self.assertEqual(json_response["user"]["username"], "CoachSteve58")
        self.assertEqual(json_response["bio"], "Head Coach and lover of sunsets")
        self.assertEqual(json_response["profile_image_url"], "asdfadsfdasdf")
        self.assertEqual(json_response["user"]["is_active"], True)
        self.assertEqual(json_response["user"]["email"], "steviewonder@gmail.com")
        
    def test_delete_player(self):
        """
        Ensure we can delete a player object.
        """
        url = '/players/8'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        