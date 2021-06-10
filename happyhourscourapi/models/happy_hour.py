from django.db import models

class HappyHour(models.Model):

    business = models.ForeignKey("Business", on_delete=models.DO_NOTHING,)
    special_type = models.ForeignKey("SpecialType", on_delete=models.DO_NOTHING,)
    weekday = models.ForeignKey("WeekDay", on_delete=models.DO_NOTHING,)
    description = models.CharField(max_length=200)
    image = models.ImageField(null=True)