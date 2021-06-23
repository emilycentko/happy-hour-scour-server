from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from happyhourscourapi.models import HappyHour, Customer, Review
from django.contrib.auth.models import User

class ReviewView(ViewSet):

    def create(self, request):
        
        customer = Customer.objects.get(user=request.auth.user)

        
        review = Review()
        review.review = request.data["review"]
        review.rating = request.data["rating"]

        happy_hour = HappyHour.objects.get(pk=request.data["happyHourId"])
        review.happy_hour = happy_hour

        # customer = Customer.objects.get(pk=request.data["customerId"])
        review.customer = customer

        try:
            review.save()

            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        
        customer = Customer.objects.get(user=request.auth.user)
        
        review = Review()
        review.review = request.data["review"]
        review.rating = request.data["rating"]

        happy_hour = HappyHour.objects.get(pk=request.data["happyHourId"])
        review.happy_hour = happy_hour

        customer = Customer.objects.get(pk=request.data["customerId"])
        review.customer = customer

        happy_hour.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        
        try:
            review = Review.objects.get(pk=pk)
            review.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Review.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        
        try:
            
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request, pk=None):
        
        happy_hour = HappyHour.objects.all()
       
        happy_hour = self.request.query_params.get('happyhour', None)

        if happy_hour is not None:
            reviews = Review.objects.filter(happy_hour__id=happy_hour)
        
        else:
            
            reviews = Review.objects.all()

        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request})

        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
        depth = 1

class CustomerSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        fields = ('user')
        depth = 1

class HappyHourSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = HappyHour
        fields = ('id', 'business', 'special_type', 'weekday', 'start_time', 'end_time', 'wine', 'beer', 'food', 'liquor', 'image')
        depth = 1

class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields = ('id', 'review', 'rating', 'happy_hour', 'customer')
        depth = 2

