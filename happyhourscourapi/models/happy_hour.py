from django.db import models

class HappyHour(models.Model):

    business = models.ForeignKey("Business", on_delete=models.DO_NOTHING,)
    special_type = models.ForeignKey("SpecialType", on_delete=models.DO_NOTHING,)
    weekday = models.ForeignKey("WeekDay", on_delete=models.DO_NOTHING,)
    wine = models.CharField(max_length=200, null=True)
    beer = models.CharField(max_length=200, null=True)
    food = models.CharField(max_length=200, null=True)
    liquor = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    start_time = models.TimeField(auto_now = False, auto_now_add = False)
    end_time = models.TimeField(auto_now = False, auto_now_add = False)

    @property
    def favorited(self):
        return self.__favorited
    
    @favorited.setter
    def favorited(self, value):
            self.__favorited = value