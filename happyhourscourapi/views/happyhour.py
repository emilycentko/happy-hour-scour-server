from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from happyhourscourapi.models import HappyHour, Customer


class HappyHourView(ViewSet):

    def list(self, request):

        happy_hours = HappyHour.objects.all()

        special_type = self.request.query_params.get('type', None)
        if special_type is not None:
            happy_hours = happy_hours.filter(special_type__id=special_type)

        serializer = HappyHourSerializer(
            happy_hours, many=True, context={'request': request})
        return Response(serializer.data)

class HappyHourSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'description', 'image')
        depth = 1