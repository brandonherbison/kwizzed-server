from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Category


class CategoryView(ViewSet):
    """Category View"""

    def retrieve(self, request, pk):

        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label',)