from django.db import models

class Time(models.Model):

    happy_hour = models.ForeignKey("HappyHour", on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now = False, auto_now_add = False)
    end_time = models.TimeField(auto_now = False, auto_now_add = False)