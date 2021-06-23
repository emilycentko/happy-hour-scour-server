from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from happyhourscourapi.models import HappyHour, Customer, Favorite 
from datetime import datetime as date

class FavoriteView(ViewSet):

    def list(self, request):

        
        customer = Customer.objects.get(user=request.auth.user)
        favorites = Favorite.objects.filter(customer=customer)

        serializer = FavoriteSerializer(
            favorites, many=True, context={'request': request})

        return Response(serializer.data)

    def create(self, request):

        customer = Customer.objects.get(user=request.auth.user)

        favorite = Favorite()
        favorite.customer = customer
        happy_hour = HappyHour.objects.get(pk=request.data["happy_hour"])
        favorite.happy_hour = happy_hour

        try:
            favorite.save()
            serializer = FavoriteSerializer(favorite, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):

        customer = Customer.objects.get(user=request.auth.user)

        try:
            favorite = Favorite.objects.get(happy_hour_id=pk, customer=customer)
            favorite.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Favorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserSerializer(serializers.HyperlinkedModelSerializer):
   
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1

class CustomerSerializer(serializers.ModelSerializer):
 
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'user',)

class FavoriteHappyHourSerializer(serializers.ModelSerializer):

    start_time=serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p',)
    end_time=serializers.TimeField(format='%I:%M %p', input_formats='%I:%M %p',)
   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'start_time', 'end_time', 'wine', 'beer', 'food', 'liquor', 'image')
        depth = 1

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):

    happy_hour = FavoriteHappyHourSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ('id', 'happy_hour')
        depth = 2
