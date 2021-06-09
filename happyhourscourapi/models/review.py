from happyhourscourapi.models import happy_hour
from django.db import models

class Review(models.Model):

    rating = models.IntegerField()
    review = models.CharField(max_length=200)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    happy_hour = models.ForeignKey("HappyHour", on_delete=models.CASCADE)