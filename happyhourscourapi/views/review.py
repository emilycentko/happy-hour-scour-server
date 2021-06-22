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

        customer = Customer.objects.get(pk=request.data["customerId"])
        review.customer = customer

        try:
            review.save()

            serializer = ReviewSerializer(review, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    

class ReviewSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Review
        fields = ('id', 'review', 'rating', 'happy_hour', 'customer')
        depth = 1

