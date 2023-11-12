# models.py

from django.db import models

class Comment(models.Model):
    comment_text = models.TextField()
    sentiment = models.CharField(max_length=255)
    probability_positive = models.FloatField()  # Adjust based on your model
    probability_negative = models.FloatField()  # Adjust based on your model

    def __str__(self):
        return self.comment_text
