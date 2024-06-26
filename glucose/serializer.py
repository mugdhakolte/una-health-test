from rest_framework import serializers

from glucose.models import Device, GlucoseLevel, User


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
        fields = "__all__"


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class GlucoseLevelMixMaxSerializer(serializers.Serializer):
    min_glucose_level = serializers.IntegerField()
    max_glucose_level = serializers.IntegerField()
