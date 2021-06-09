from django.db import models

class Favorite(models.Model):

    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    happy_hour = models.ForeignKey("HappyHour", on_delete=models.CASCADE, related_name='favorited_happy_hour')