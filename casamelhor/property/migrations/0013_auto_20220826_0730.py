# Generated by Django 3.2.13 on 2022-08-26 07:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0012_auto_20220826_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='address',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='br_name',
        ),
    ]