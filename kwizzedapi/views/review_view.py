from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Review, Player
from datetime import date


class ReviewView(ViewSet):
    """Review View"""

    def retrieve(self, request, pk):

        review = Review.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        review = Review.objects.all()
        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Review instance
        """
        
        new_review = Review()
        new_review.body = request.data["body"]
        new_review.player = Player.objects.get(user=request.auth.user)
        new_review.date_posted = date.today()
        new_review.save()

        serializer = ReviewSerializer(new_review, context={'request': request})

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single review

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PlayerReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for player reviews

    Arguments:
        serializers
    """
    class Meta:
        model = Player
        fields = ('id', 'full_name')

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializers
    """
    player = PlayerReviewSerializer(many=False)
    
    class Meta:
        model = Review
        fields = ('id', 'body', 'player', 'date_posted')