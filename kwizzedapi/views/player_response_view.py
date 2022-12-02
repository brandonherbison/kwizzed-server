from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import PlayerResponse


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

class PlayerResponseSerializer(serializers.ModelSerializer):
    """JSON serializer for playerResponses

    Arguments:
        serializers
    """
    class Meta:
        model = PlayerResponse
        fields = ('id', 'player', 'answer',)