from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Player
from django.contrib.auth.models import User


class PlayerView(ViewSet):
    """Player View"""

    def retrieve(self, request, pk):

        player = Player.objects.get(pk=pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        player = Player.objects.all()
        serializer = PlayerSerializer(player, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "is_staff", "email", "is_active")


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)
    class Meta:
        model = Player
        fields = ('id', 'user', 'bio', 'profile_image_url',)