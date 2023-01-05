import json
from rest_framework import status
from rest_framework.test import APITestCase
from kwizzedapi.models import Player
from rest_framework.authtoken.models import Token


class AnswerTests(APITestCase):
    
    fixtures = ['categories', 'questions', 'answers', 'players', 'player_responses', 'users', 'tokens']
    
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_answer(self):
        """
        Ensure we can create a new answer object.
        """
        url = '/answers'
        data = {
            "answerText": "This is a test answer",
            "questionId": 1,
            "isCorrect": True
        }
        response = self.client.post(url, data, format='json')
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["answer_text"], "This is a test answer")
        self.assertEqual(json_response["question"], 1)
        self.assertEqual(json_response["is_correct"], True)
        
    def test_get_answer(self):
        """
        Ensure we can get an answer object.
        """
        url = '/answers/1'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["answer_text"], "Apollo 11")
        self.assertEqual(json_response["question"], 1)
        self.assertEqual(json_response["is_correct"], True)
        
    def test_get_answers(self):
        """
        Ensure we can get all answer objects.
        """
        url = '/answers'
        response = self.client.get(url)
        
        json_response = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 340)
    
