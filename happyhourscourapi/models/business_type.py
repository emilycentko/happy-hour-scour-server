from django.db import models

class BusinessType(models.Model):

    type = models.CharField(max_length=50)