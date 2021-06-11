from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from happyhourscourapi.models import WeekDay

class WeekDayView(ViewSet):

    def list(self, request):
        weekdays = WeekDay.objects.all()

        serializer = WeekDaySerializer(
            weekdays, many=True, context={'request': request})
        return Response(serializer.data)

class WeekDaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeekDay
        fields = ('id', 'day')