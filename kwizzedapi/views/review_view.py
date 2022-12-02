from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Review


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

class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for reviews

    Arguments:
        serializers
    """
    class Meta:
        model = Review
        fields = ('id', 'body', 'player', 'date_posted')