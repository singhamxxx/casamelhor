from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = "__all__"


class AmenitiesGroupSerializer(serializers.ModelSerializer):
    amenity = AmenitiesSerializer(read_only=True)

    class Meta:
        model = AmenitiesGroup
        fields = ('id', 'name', 'is_active', 'amenity', 'amenity_id')
        extra_kwargs = {'amenity_id': {'source': 'amenity', 'write_only': True}}


class AmenitiesAttributeSerializer(serializers.ModelSerializer):
    amenity_group = AmenitiesGroupSerializer(read_only=True)

    class Meta:
        model = AmenitiesAttribute
        fields = ['id', 'name', 'is_active', 'amenity_group', 'amenity_group_id', 'image']
        extra_kwargs = {'amenity_group_id': {'source': 'amenity_group', 'write_only': True}}
