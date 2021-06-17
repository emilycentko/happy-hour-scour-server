from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from happyhourscourapi.models import HappyHour, Customer, Favorite
from django.contrib.auth.models import User
from datetime import datetime as date
from rest_framework.decorators import action
from django.db.models import Q


class HappyHourView(ViewSet):

    def list(self, request):

        happy_hours = HappyHour.objects.all()
        customer = Customer.objects.get(user=request.auth.user)

        for happy_hour in happy_hours:
            happy_hour.favorited = None

            try:
                Favorite.objects.get(happy_hour=happy_hour, customer=customer)
                happy_hour.favorited = True
            except Favorite.DoesNotExist:
                happy_hour.favorited = False


        #Params for today, day of the week, and search query 

        day = self.request.query_params.get('day', None)

        search_terms = self.request.query_params.get('searchTerms', None)

        if day is not None:
            happy_hours = happy_hours.filter(weekday__day=day)
        
        else:
            today = date.today().strftime("%A")
            happy_hours = happy_hours.filter(weekday__day=today)

        if search_terms is not None:
            today = date.today().strftime("%A")
            happy_hours = HappyHour.objects.filter(Q(business__name__contains=search_terms, weekday__day=today))

        if search_terms is not None and day is not None:
            happy_hours = HappyHour.objects.filter(Q(business__name__contains=search_terms, weekday__day=day))

        #Params for special type
        
        special_type = self.request.query_params.get('type', None)

        if special_type is not None:
            happy_hours = happy_hours.filter(special_type__id=special_type)

        serializer = HappyHourSerializer(
            happy_hours, many=True, context={'request': request})
        return Response(serializer.data)
    
    

class HappyHourSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'description', 'image', 'favorited')
        depth = 1


