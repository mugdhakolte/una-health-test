# Generated by Django 5.0.5 on 2024-05-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("glucose", "0002_alter_glucoselevel_options_and_more"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="device",
            index=models.Index(fields=["name"], name="Device_name_83218f_idx"),
        ),
        migrations.AddIndex(
            model_name="device",
            index=models.Index(fields=["serial_no"], name="Device_serial__eb569e_idx"),
        ),
        migrations.AddIndex(
            model_name="glucoselevel",
            index=models.Index(
                fields=["device_timestamp"], name="GlucoseLeve_device__1504ef_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["user_id"], name="User_user_id_d2ee54_idx"),
        ),
    ]
