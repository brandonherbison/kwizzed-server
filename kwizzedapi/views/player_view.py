from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Player, PlayerResponse, Answer
from django.contrib.auth.models import User


class PlayerView(ViewSet):
    """Player View"""

    def retrieve(self, request, pk):
        if pk == "current":
            user = request.user
            player = Player.objects.get(user=user)
            data = {
                'username' : user.username,
                'firstName' : user.first_name,
                'lastName' : user.last_name,
                'email' : user.email,
                'isStaff' : user.is_staff,
                'isActive' : user.is_active,
                'id' : player.id,
                'bio' : player.bio,
                'profileImageUrl' : player.profile_image_url,
            }
            return Response(data, status=status.HTTP_200_OK)

        player = Player.objects.get(pk=pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        players = Player.objects.all()
        
        
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """Handle PUT requests for a player

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(pk=pk)
        user = User.objects.get(pk=player.user_id)
        
        user.username = request.data["username"]
        user.email = request.data["email"]
        user.is_active = request.data["isActive"]
        player.bio = request.data["bio"]
        player.profile_image_url = request.data["profileImageUrl"]
        user.save()
        player.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single player

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            player = Player.objects.get(pk=pk)
            player.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Player.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "is_staff", "email", "is_active",)


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)
    class Meta:
        model = Player
        fields = ('id', 'full_name', "user", "bio", 'profile_image_url', 'response_count', 'correct_response_count')