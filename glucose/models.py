from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    """
    Class representing User Model.
    """

    user_id = models.UUIDField(editable=False, unique=True)

    USERNAME_FIELD = "user_id"

    class Meta:
        """Meta class for User."""

        db_table = "User"
        indexes = [
            models.Index(fields=["user_id"]),
        ]

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
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["serial_no"]),
        ]

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
    recording_type = models.IntegerField(blank=True, null=True)
    glucose_value_history = models.IntegerField(blank=True, null=True)
    glukose_scan_mg_dL = models.IntegerField(blank=True, null=True)
    nicht_numerisches_schnellwirkendes_insulin = models.IntegerField(
        blank=True, null=True
    )
    schnellwirkendes_insulin = models.IntegerField(blank=True, null=True)
    nicht_numerische_nahrungsdaten = models.IntegerField(blank=True, null=True)
    kohlenhydrate_gramm = models.IntegerField(blank=True, null=True)
    kohlenhydrate_portionen = models.IntegerField(blank=True, null=True)
    nicht_numerisches_depotinsulin = models.IntegerField(blank=True, null=True)
    depotinsulin = models.IntegerField(blank=True, null=True)
    notizen = models.IntegerField(blank=True, null=True)
    glukose_teststreifen_mg_dL = models.IntegerField(blank=True, null=True)
    keton_mmol_L = models.IntegerField(blank=True, null=True)
    mahlzeiteninsulin = models.IntegerField(blank=True, null=True)
    korrekturinsulin = models.IntegerField(blank=True, null=True)
    insulin_anderung_durch_anwender = models.IntegerField(blank=True, null=True)

    class Meta:
        """Meta class for GlucoseLevel."""

        db_table = "GlucoseLevel"
        ordering = ["-device_timestamp"]
        indexes = [
            models.Index(fields=["device_timestamp"]),
        ]

    def __str__(self):
        """
        device, device_timestamp
        :return: GlucoseLevel
        """
        return f"{self.device}-{self.device_timestamp}"
