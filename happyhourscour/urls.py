from rest_framework import routers
from happyhourscourapi.views import HappyHourView, Profile
from django.conf.urls import include
from django.urls import path
from happyhourscourapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'happyhours', HappyHourView, 'happyhour')
router.register(r'profile', Profile, 'profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]