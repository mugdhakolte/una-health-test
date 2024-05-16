from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from glucose.models import Device, GlucoseLevel, User


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id="test_user")
        self.device = Device.objects.create(
            name="test_device", serial_no="123456", user=self.user
        )
        self.glucose_level = GlucoseLevel.objects.create(
            device=self.device,
            device_timestamp=timezone.make_aware(
                datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
            ),
        )

    def test_user_creation(self):
        self.assertEqual(self.user.user_id, "test_user")

    def test_device_creation(self):
        self.assertEqual(self.device.name, "test_device")
        self.assertEqual(self.device.serial_no, "123456")
        self.assertEqual(self.device.user, self.user)

    def test_glucose_level_creation(self):
        self.assertEqual(self.glucose_level.device, self.device)
        self.assertEqual(
            str(self.glucose_level.device_timestamp), "2022-01-01 12:00:00+00:00"
        )

    def test_list_glucose_levels(self):
        client = APIClient()
        url = reverse("levels-list")
        response = client.get(url, {"user_id": self.user.user_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 1)

    def test_retrieve_glucose_levels(self):
        client = APIClient()
        url = reverse("levels-detail", kwargs={"pk": self.glucose_level.pk})
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
