from django.db import models

class Review(models.Model):

    body = models.CharField(max_length=200)
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    date_posted = models.DateField()
