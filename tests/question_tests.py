import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token

class QuestionTests(APITestCase):
    
    fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens']
    
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_question(self):
        """
        Ensure we can create a new question object.
        """
        url = '/questions'
        data = {
            "questionText": "This is a test question",
            "categoryId": 1,
            "isPractice": False,
            "difficultyLevel": "easy",
            "playerId": 1
            
        }
        response = self.client.post(url, data, format='json')
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["question_text"], "This is a test question")
        self.assertEqual(json_response["category"], {"id": 1, "label": "Science and Nature"})
        self.assertEqual(json_response["is_practice"], False)
        self.assertEqual(json_response["difficulty_level"], "easy")
        self.assertEqual(json_response["player"], {'id': 1, 'full_name': 'Brandon Herbison'})
        
    def test_get_question(self):
        """
        Ensure we can get a question object.
        """
        url = '/questions/1'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["question_text"], "Which Apollo mission was the first one to land on the Moon?")
        self.assertEqual(json_response["category"], {"id": 1, "label": "Science and Nature"})
        self.assertEqual(json_response["is_practice"], True)
        self.assertEqual(json_response["difficulty_level"], "easy")
        self.assertEqual(json_response["player"], {"id": 4, "full_name": "Jonathan Woodard"})
        self.assertEqual(json_response["answers"], [{"id": 1, "answer_text": "Apollo 11", "is_correct": True}, {"id": 2, "answer_text": "Apollo 10", "is_correct": False}, {"id": 3, "answer_text": "Apollo 9", "is_correct": False}, {"id": 4, "answer_text": "Apollo 13", "is_correct": False}])
        
    def test_get_questions(self):
        """
        Ensure we can get all question objects.
        """
        url = '/questions'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 0)
        
    def test_delete_question(self):
        """
        Ensure we can delete a question object.
        """
        url = '/questions/1'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)