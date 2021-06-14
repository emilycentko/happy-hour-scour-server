from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from happyhourscourapi.models import Customer

class Profile(ViewSet):

    def list(self, request):

        customer = Customer.objects.get(user=request.auth.user)

        customer = CustomerSerializer(
            customer, many=False, context={'request': request})

        profile = {}
        profile["customer"] = customer.data

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class CustomerSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        fields = ('user', 'bio')