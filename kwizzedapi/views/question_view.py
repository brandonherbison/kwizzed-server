from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Question, Answer, Category


class QuestionView(ViewSet):
    """Question View"""

    def retrieve(self, request, pk):

        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):

        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def create(self, request): 
        """Handle POST operations
        Returns:
            Response -- JSON serialized Question instance
        """
        category = Category.objects.get(pk=request.data['categoryId'])
        
        new_question = Question()
        new_question.question_text = request.data["questionText"]
        new_question.difficulty_level = request.data["difficultyLevel"]
        new_question.is_practice = request.data["isPractice"]
        new_question.category = category
        new_question.save()

        serializer = QuestionSerializer(new_question, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AnswerSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Answer
        fields = ('answer_text', 'is_correct',)

class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializers
    """
    answers = AnswerSerializer(many=True)
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'is_practice', 'category', 'difficulty_level', 'answers')
        depth = 1