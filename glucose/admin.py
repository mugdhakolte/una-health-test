from django.contrib import admin

from glucose.models import User, Device, GlucoseLevel


class UserAdmin(admin.ModelAdmin):
    search_fields = [
        "user_id",
    ]
    list_per_page = 50


class DeviceAdmin(admin.ModelAdmin):
    search_fields = [
        "serial_no",
        "name",
        "user__user_id",
    ]
    list_per_page = 50


class GlucoseLevelAdmin(admin.ModelAdmin):
    search_fields = [
        "device__user__user_id",
        "device__name",
        "device__serial_no",
        "device_timestamp",
        "recording_type",
    ]
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(GlucoseLevel, GlucoseLevelAdmin)
