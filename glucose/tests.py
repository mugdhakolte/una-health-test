from django.test import TestCase

from glucose.models import User, Device, GlucoseLevel


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(user_id="test_user")
        self.device = Device.objects.create(
            name="test_device", serial_no="123456", user=self.user
        )
        self.glucose_level = GlucoseLevel.objects.create(
            device=self.device, device_timestamp="2022-01-01 12:00:00"
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
            str(self.glucose_level.device_timestamp), "2022-01-01 12:00:00"
        )
