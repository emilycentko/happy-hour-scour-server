from django.db import models

class SpecialType(models.Model):

    type = models.CharField(max_length=50)