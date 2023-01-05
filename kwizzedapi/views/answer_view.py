from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Answer, Question


class AnswerView(ViewSet):
    """Answer View"""

    def retrieve(self, request, pk):
        """Handles GET requests for single answer"""

        answer = Answer.objects.get(pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handles GET requests to answer resource"""

        answer = Answer.objects.all()
        serializer = AnswerSerializer(answer, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handles POST operations for answers

        Returns:
            Response -- JSON serialized Answer instance
        """
        question = Question.objects.get(pk=request.data['questionId'])
        
        new_answer = Answer()
        new_answer.answer_text = request.data["answerText"]
        new_answer.is_correct = request.data["isCorrect"]
        new_answer.question = question
        new_answer.save()

        serializer = AnswerSerializer(new_answer, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handles PUT requests for an answer 

        Returns:
            Response -- Empty body with 204 status code
        """
        question = Question.objects.get(pk=request.data['questionId'])
        
        answer = Answer.objects.get(pk=pk)
        answer.answer_text = request.data["answerText"]
        answer.is_correct = request.data["isCorrect"]
        answer.question = question
        answer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class AnswerSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'is_correct', 'question')