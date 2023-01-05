import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token



class CategoryTests(APITestCase):
    
    fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens']
    
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_category(self):
        """
        Ensure we can create a new category object.
        """
        url = '/categories'
        data = {
            "label": "Test Category"
        }
        response = self.client.post(url, data, format='json')
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Test Category")
        
    def test_get_category(self):
        """
        Ensure we can get a category object.
        """
        url = '/categories/1'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Science and Nature")
        
    def test_delete_category(self):
        """
        Ensure we can delete a category object.
        """
        url = '/categories/1'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_get_all_categories(self):
        """
        Ensure we can get all category objects.
        """
        url = '/categories'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 5)

