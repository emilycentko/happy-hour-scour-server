from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from happyhourscourapi.models import Location

class LocationView(ViewSet):

    def list(self, request):
        locations = Location.objects.all()

        serializer = LocationSerializer(
            locations, many=True, context={'request': request})
        return Response(serializer.data)

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = ('id', 'name')