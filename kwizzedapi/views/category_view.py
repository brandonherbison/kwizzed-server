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
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Category instance
        """
        new_category = Category()
        new_category.label = request.data["label"]
        new_category.save()

        serializer = CategorySerializer(new_category, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label',)