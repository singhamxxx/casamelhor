# Generated by Django 3.2.13 on 2022-06-30 10:55

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20220630_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='vault',
            name='ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20, verbose_name='Image PPOI'),
        ),
    ]
