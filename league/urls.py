from django.urls import path, include
from rest_framework import routers

from league import views


router = routers.DefaultRouter()
router.register(r"summoners", views.SummonerViewset, basename="summoner")

urlpatterns = [path("", include(router.urls))]
