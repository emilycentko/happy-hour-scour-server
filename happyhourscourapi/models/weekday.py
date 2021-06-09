from django.db import models

class WeekDay(models.Model):

    day = models.CharField(max_length=50)