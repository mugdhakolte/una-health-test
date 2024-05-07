from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from glucose.viewset import LevelViewset


router = routers.DefaultRouter()
router.register(r"levels", LevelViewset, basename="levels")

urlpatterns = [
    path("", include(router.urls)),
]
