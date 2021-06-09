from django.db import models

class Business(models.Model):

    name = models.CharField(max_length=60)
    business_type = models.ForeignKey("BusinessType", on_delete=models.DO_NOTHING,)
    patio = models.BooleanField(default=False)
    location = models.CharField(max_length=50)
    trivia = models.BooleanField(default=False)