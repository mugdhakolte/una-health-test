import uuid
from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from glucose.models import Device, GlucoseLevel, User


class ModelTestCase(TestCase):
    def setUp(self):
        self.filepath = "sample-data/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa.csv"
        self.user_id = uuid.UUID(self.filepath.split("/")[1].split(".")[0])
        self.user = User.objects.create(user_id=uuid.uuid4())
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
        self.assertIsInstance(self.user.user_id, uuid.UUID)
        self.assertEqual(self.user, User.objects.get(user_id=self.user.user_id))

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

    def test_create_same_user_file(self):
        client = APIClient()
        url = reverse("data-list")
        with open(self.filepath, "rb") as f:
            file = SimpleUploadedFile(self.filepath, f.read())
            response = client.post(url, {"file": file}, format="multipart")

        self.assertEqual(User.objects.get(user_id=self.user_id).user_id, self.user_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
