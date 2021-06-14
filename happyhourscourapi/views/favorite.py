from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from happyhourscourapi.models import HappyHour, Customer, Favorite 

# class Favorite(ViewSet)

#     permission_classes = (IsAuthenticatedOrReadOnly,)

#     def list(self, request):