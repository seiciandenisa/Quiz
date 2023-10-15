from django.db import models


# Create your models here.

class Quiz(models.Model):
    class Difficulty(models.TextChoices):
        EASY = 'easy'
        MEDIUM = 'medium'
        HARD = 'hard'

    difficult = models.CharField(choices=Difficulty.choices, max_length=50)
    number_of_questions = models.IntegerField
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
