from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Answer


class AnswerView(ViewSet):
    """Answer View"""

    def retrieve(self, request, pk):

        answer = Answer.objects.get(pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        answer = Answer.objects.all()
        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class AnswerSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'is_correct', 'question')