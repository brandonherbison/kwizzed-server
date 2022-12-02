from django.db import models

class Answer(models.Model):

    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")