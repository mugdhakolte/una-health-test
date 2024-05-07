from django.db import models


class User(models.Model):
    """
    Class representing User Model.
    """

    user_id = models.CharField(max_length=100)

    class Meta:
        """Meta class for User."""

        db_table = "User"

    def __str__(self):
        """
        User
        :return: user
        """
        return f"{self.user_id}"


class Device(models.Model):
    """
    Class representing Device Model.
    """

    name = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta class for Device."""

        db_table = "Device"

    def __str__(self):
        """
        Device name and serial no
        :return: user
        """
        return f"{self.user}-{self.name}-{self.serial_no}"


class GlucoseLevel(models.Model):
    """
    Class representing GlucoseLevel Model.
    """

    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    device_timestamp = models.DateTimeField()
    recording_type = models.IntegerField()
    glucose_value_history = models.IntegerField()
    details = models.JSONField()

    class Meta:
        """Meta class for GlucoseLevel."""

        db_table = "GlucoseLevel"
        ordering = ["-device_timestamp"]

    def __str__(self):
        """
        device, device_timestamp
        :return: GlucoseLevel
        """
        return f"{self.device}-{self.device_timestamp}"
