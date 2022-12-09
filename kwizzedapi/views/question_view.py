from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from kwizzedapi.models import Question, Answer, Category, Player
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import random


class QuestionView(ViewSet):
    """Question View"""

    def retrieve(self, request, pk):

        question = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        player = Player.objects.get(user=request.auth.user)
        questions = Question.objects.filter(player=player)
        category = request.query_params.get("category", None)
        if category is not None:
            filtered_questions = list(Question.objects.filter(is_approved=True and category==category))
            questions = random.sample(filtered_questions, 10)
            random.shuffle(questions)
            serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
            
        elif "practice" in request.query_params:
            filtered_questions = list(Question.objects.filter(is_practice=request.query_params["practice"]))
            questions = random.sample(filtered_questions, 5)
            random.shuffle(questions)
            serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
        
        elif "player" in request.query_params:
            filtered_questions = list(Question.objects.filter(player=request.query_params["player"]))
            questions = filtered_questions
            serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
        
        elif "approved" in request.query_params:
            filtered_questions = list(Question.objects.filter(is_approved=request.query_params["approved"]))
            questions = filtered_questions
            serializer = QuestionSerializer(questions, many=True, context={'request': request})
            return Response(serializer.data , status=status.HTTP_200_OK)
        

            
        
        
        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data , status=status.HTTP_200_OK)

    
    def create(self, request): 
        """Handle POST operations
        Returns:
            Response -- JSON serialized Question instance
        """
        category = Category.objects.get(pk=request.data['categoryId'])
        player = Player.objects.get(user=request.auth.user)
        
        new_question = Question()
        new_question.question_text = request.data["questionText"]
        new_question.difficulty_level = request.data["difficultyLevel"]
        new_question.is_practice = False
        new_question.category = category
        new_question.player = player
        new_question.is_approved = False
        new_question.save()

        serializer = QuestionSerializer(new_question, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a question
        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=request.data['categoryId'])
        
        question = Question.objects.get(pk=pk)
        question.question_text = request.data["questionText"]
        question.difficulty_level = request.data["difficultyLevel"]
        question.is_practice = request.data["isPractice"]
        question.is_approved = request.data["isApproved"]
        question.category = category
        question.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single question
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            question = Question.objects.get(pk=pk)
            question.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Question.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class AnswerSerializer(serializers.ModelSerializer):
    """JSON serializer for answers

    Arguments:
        serializers
    """
    class Meta:
        model = Answer
        fields = ('id', 'answer_text', 'is_correct',)
        
class QuestionPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializers
    """
    class Meta:
        model = Player
        fields = ('id', 'full_name')
        depth = 1

class QuestionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializers
    """

    answers = AnswerSerializer(many=True)
    player = QuestionPlayerSerializer(many=False)
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'is_practice', 'category', 'difficulty_level', 'answers', 'is_approved', 'player')
        depth = 1
        
