from django.urls import include, path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from applications.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    round = SimpleRouter()


router.register("users", UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]