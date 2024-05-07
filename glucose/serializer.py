from rest_framework import serializers

from models import User, GlucoseLevel, Device


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "user_id"]


class DeviceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Device
        fields = ["id", "name", "serial_no", "user"]


class GlucoseLevelSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()

    class Meta:
        model = GlucoseLevel
        fields = [
            "id",
            "device",
            "device_timestamp",
            "recording_type",
            "glucose_value_history",
            "details",
        ]
