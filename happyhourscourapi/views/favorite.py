from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from happyhourscourapi.models import HappyHour, Customer, Favorite 

class FavoriteView(ViewSet):

    def list(self, request):

        try:
            customer = Customer.objects.get(user=request.auth.user)
            favorites = Favorite.objects.filter(customer=customer)

            serializer = FavoriteSerializer(
                favorites, many=True, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['get', 'post'], detail=False)
    def favorites(self, request):

        customer = Customer.objects.get(user=request.auth.user)
        favorites = Favorite.objects.filter(customer=customer)

        if request.method == "GET":

            serializer = FavoriteSerializer(
                favorites, many=True, context={'request': request})
            return Response(serializer.data)

        if request.method == "POST":

            favorite = Favorite()

            try:
                favorite.happy_hour = Customer.objects.get(user_id=request.data["happy_hour"])
                favorite.customer = customer
                favorite.save()

                serializer = FavoriteSerializer(
                    favorite, many=False, context={'request': request})
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

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
   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'description', 'image')
        depth = 1

class FavoriteSerializer(serializers.HyperlinkedModelSerializer):

    happy_hour = FavoriteHappyHourSerializer(many=False)

    class Meta:
        model = Favorite
        fields = ('id', 'happy_hour')
        depth = 2
