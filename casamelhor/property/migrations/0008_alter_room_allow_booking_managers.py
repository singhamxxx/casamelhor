# Generated by Django 3.2.13 on 2022-08-20 04:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0007_alter_room_allow_booking_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='allow_booking_managers',
            field=models.ManyToManyField(blank=True, related_name='room_allow_booking_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]