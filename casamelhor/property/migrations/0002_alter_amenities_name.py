# Generated by Django 3.2.13 on 2022-07-05 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenities',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
