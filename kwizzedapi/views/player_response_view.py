from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import PlayerResponse, Player, Answer, Question
import statistics


class PlayerResponseView(ViewSet):
    """PlayerResponse View"""

    def retrieve(self, request, pk):

        playerResponse = PlayerResponse.objects.get(pk=pk)
        serializer = PlayerResponseSerializer(playerResponse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        

        playerResponse = PlayerResponse.objects.all()
        player = self.request.query_params.get('player', None)
        category = self.request.query_params.get('category', None)
        correct = self.request.query_params.get('correct', None)
        question = self.request.query_params.get('question', None)
        
        if player is not None and category is None:
            playerResponse = playerResponse.filter(player__id=player)
            playerResponse = playerResponse.order_by('-id')[:10]
            serializer = PlayerResponseSerializer(playerResponse, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif player is not None and category is not None:
            playerResponse = playerResponse.filter(player__id=player)
            playerResponse = playerResponse.filter(answer__question__category__id=category)
            correct_responses = playerResponse.filter(answer__is_correct=True)
            category_count = correct_responses.count()
            return Response(category_count, status=status.HTTP_200_OK)
        
        elif player is None and category is not None and correct is not None:
            playerResponse = playerResponse.filter(answer__question__category__id=category)
            correct_responses = playerResponse.filter(answer__is_correct=True)
            correct_count = correct_responses.count()
            percent_correct = round(correct_count / playerResponse.count() * 100)
            return Response(percent_correct, status=status.HTTP_200_OK)
        
        elif player is None and category is not None and correct is None and question is None:
            playerResponses = playerResponse.filter(answer__question__category__id=category)
            incorrect_responses = playerResponses.filter(answer__is_correct=False)
            missed_questions = incorrect_responses.values_list('answer__question__id', flat=True)
            most_missed = statistics.mode(missed_questions)
            question_body = Question.objects.get(pk=most_missed)
            serializer = QuestionSerializer(question_body, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
            
        
        
        serializer = PlayerResponseSerializer(playerResponse, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def create(self, request): 
        """Handle POST operations
        Returns:
            Response -- JSON serialized Player_response instance
        """
        
        player = Player.objects.get(pk=request.data['playerId'])
        try:
            answer = Answer.objects.get(pk=request.data['answerId'])
        except Answer.DoesNotExist:
            answer = None
            
        
        new_player_response = PlayerResponse()
        new_player_response.player = player
        new_player_response.answer = answer
        new_player_response.save()

        serializer = PlayerResponseSerializer(new_player_response, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializers
    """
    class Meta:
        model = Question
        fields = ('question_text',)
    
class AnswerQuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Question
        fields = ('question_text', 'category')
    
class AnswerPlayerResponseSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    question = AnswerQuestionSerializer(many=False)
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'is_correct', 'question',)

class PlayerResponseSerializer(serializers.ModelSerializer):
    """JSON serializer for playerResponses

    Arguments:
        serializers
    """
    answer = AnswerPlayerResponseSerializer(many=False)
    
    class Meta:
        model = PlayerResponse
        fields = ('id', 'player', 'answer',)