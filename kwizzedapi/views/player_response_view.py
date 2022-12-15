from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import PlayerResponse, Player, Answer, Question


class PlayerResponseView(ViewSet):
    """PlayerResponse View"""

    def retrieve(self, request, pk):

        playerResponse = PlayerResponse.objects.get(pk=pk)
        serializer = PlayerResponseSerializer(playerResponse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        

        playerResponse = PlayerResponse.objects.all()
        
        most_recent = request.query_params.get("recent", None)
        if most_recent is not None:
            playerResponse = PlayerResponse.objects.filter(player=most_recent).order_by('-id')[:1]
            serializer = PlayerResponseSerializer(playerResponse, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        
        serializer = PlayerResponseSerializer(playerResponse, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def create(self, request): 
        """Handle POST operations
        Returns:
            Response -- JSON serialized Player_response instance
        """
        player = Player.objects.get(pk=request.data['playerId'])
        answer = Answer.objects.get(pk=request.data["answerId"])
        
        new_player_response = PlayerResponse()
        new_player_response.player = player
        new_player_response.answer = answer
        new_player_response.save()

        serializer = PlayerResponseSerializer(new_player_response, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AnswerQuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Question
        fields = ('question_text',)
    
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