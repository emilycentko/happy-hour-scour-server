from django.contrib import admin
from .models.customer import Customer
from .models.business import Business
from .models.weekday import WeekDay
from .models.business_type import BusinessType
from .models.happy_hour import HappyHour
from .models.favorite import Favorite
from .models.special_type import SpecialType
from .models.review import Review
from .models.location import Location

# Register your models here.

admin.site.register(HappyHour)
admin.site.register(Favorite)