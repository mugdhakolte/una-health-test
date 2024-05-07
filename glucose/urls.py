from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from glucose.viewset import LevelViewset, DataViewset


router = routers.DefaultRouter()
router.register(r"data", DataViewset, basename="data")
# router.register(r"levels", LevelViewset, basename="levels")

urlpatterns = [
    path("", include(router.urls)),
]
