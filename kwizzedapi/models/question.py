from django.db import models

class Question(models.Model):

    question_text = models.CharField(max_length=200)
    is_practice = models.BooleanField(default=False)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=20)
