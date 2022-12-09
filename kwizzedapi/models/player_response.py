from django.db import models

class PlayerResponse(models.Model):

    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    