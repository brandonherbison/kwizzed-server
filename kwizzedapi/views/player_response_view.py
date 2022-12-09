from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import PlayerResponse, Player, Answer


class PlayerResponseView(ViewSet):
    """PlayerResponse View"""

    def retrieve(self, request, pk):

        playerResponse = PlayerResponse.objects.get(pk=pk)
        serializer = PlayerResponseSerializer(playerResponse)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        playerResponse = PlayerResponse.objects.all()
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

class PlayerResponseSerializer(serializers.ModelSerializer):
    """JSON serializer for playerResponses

    Arguments:
        serializers
    """
    class Meta:
        model = PlayerResponse
        fields = ('id', 'player', 'answer',)