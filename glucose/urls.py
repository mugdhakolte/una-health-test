from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from glucose.viewset import DataViewset, LevelViewset

router = routers.DefaultRouter()
router.register(r"data", DataViewset, basename="data")
router.register(r"levels", LevelViewset, basename="levels")

urlpatterns = [
    path("", include(router.urls)),
]
