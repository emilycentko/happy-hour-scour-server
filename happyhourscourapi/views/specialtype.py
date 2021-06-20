from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from happyhourscourapi.models import SpecialType

class SpecialTypeView(ViewSet):

    def list(self, request):
        specialtypes = SpecialType.objects.all()

        serializer = SpecialTypeSerializer(
            specialtypes, many=True, context={'request': request})
        return Response(serializer.data)

class SpecialTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SpecialType
        fields = ('id', 'type')