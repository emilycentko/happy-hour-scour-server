from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from happyhourscourapi.models import HappyHour, Customer, Favorite, Business
from django.contrib.auth.models import User
from datetime import datetime as date
from rest_framework.decorators import action
from django.db.models import Q
import time


class HappyHourView(ViewSet):

    def list(self, request):

        happy_hours = HappyHour.objects.all()

        #Params for today, day of the week, and search query - params check for
        # both today and day of the week

        day = self.request.query_params.get('day', None)
        today = date.today().strftime("%A")

        search_terms = self.request.query_params.get('searchTerms', None)

        if day is not None:
            happy_hours = happy_hours.filter(weekday__day=day)
        
        else:
            
            happy_hours = happy_hours.filter(weekday__day=today)

        if search_terms is not None:
            happy_hours = HappyHour.objects.filter(Q(business__name__contains=search_terms, weekday__day=today))

        if search_terms is not None and day is not None:
            happy_hours = HappyHour.objects.filter(Q(business__name__contains=search_terms, weekday__day=day))

        #Params for special type
        
        special_type = self.request.query_params.get('special_type', None)

        if special_type is not None:
            
            happy_hours = HappyHour.objects.filter(special_type__id=special_type, weekday__day=today)

        if special_type is not None and day is not None:
            happy_hours = HappyHour.objects.filter(special_type__id=special_type, weekday__day=day)

        #Params for location
        
        location = self.request.query_params.get('location', None)

        #location and today
        if location is not None:
            
            happy_hours = HappyHour.objects.filter(business__location__id=location, weekday__day=today)
        
        #location and day of the week
        if location is not None and day is not None:
            happy_hours = HappyHour.objects.filter(business__location__id=location, weekday__day=day)
        
        #location and today and special type
        if location is not None and special_type is not None:
            happy_hours = HappyHour.objects.filter(business__location__id=location, weekday__day=today, special_type__id=special_type)

        #location and day of the week and special type
        if location is not None and day is not None and special_type is not None:
            happy_hours = HappyHour.objects.filter(business__location__id=location, weekday__day=day, special_type__id=special_type)

        #Params for features
        
        trivia = self.request.query_params.get('trivia', None)

        if trivia is not None:
            happy_hours = HappyHour.objects.filter(business__trivia=True, weekday__day=today)

        if trivia is not None and day is not None:
            happy_hours = HappyHour.objects.filter(business__trivia=True, weekday__day=day)

        patio = self.request.query_params.get('patio', None)

        if patio is not None:
            happy_hours = HappyHour.objects.filter(business__patio=True, weekday__day=today)

        if patio is not None and day is not None:
            happy_hours = HappyHour.objects.filter(business__patio=True, weekday__day=day)

        #Favorited property - loops over happy_hours to make them not favorited by default, unless
        #True, then added to Favorite table 
        
        customer = Customer.objects.get(user=request.auth.user)

        for happy_hour in happy_hours:
            happy_hour.favorited = None

            try:
                Favorite.objects.get(happy_hour=happy_hour, customer=customer)
                happy_hour.favorited = True
            except Favorite.DoesNotExist:
                happy_hour.favorited = False


        serializer = HappyHourSerializer(
            happy_hours, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        
        try:
            happy_hour = HappyHour.objects.get(pk=pk)
            serializer = HappyHourSerializer(happy_hour, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class BusinessSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Business
        fields = ('id', 'name', 'business_type', 'patio', 'location', 'trivia')
        depth = 1


class HappyHourSerializer(serializers.ModelSerializer):

    business = BusinessSerializer(many=False)
    
    start_time=serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p',)
    end_time=serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p',)

   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'start_time', 'end_time', 'wine', 'beer', 'food', 'liquor', 'image', 'favorited')
        depth = 1



