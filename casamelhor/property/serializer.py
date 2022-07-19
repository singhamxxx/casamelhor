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


class PropertyImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyImages
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    property_amenities = AmenitiesAttributeSerializer(read_only=True)
    images = serializers.ListField(child=serializers.FileField(allow_empty_file=True,  use_url=False), write_only=True, required=False)
    property_images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'name', 'description', 'house_number', 'building_number', 'area', 'city', 'country', 'state', 'zipcode', 'latitude',
                  'longitude', 'numbers_of_rooms', 'check_in_time', 'check_out_time', 'house_role', 'property_amenities', 'allow_booking_managers',
                  'property_amenities_id', 'created_at', 'updated_at', 'images', 'property_images']
        extra_kwargs = {'property_amenities_id': {'source': 'property_amenities', 'write_only': True}}
    
    def get_property_images(self, obj):
        return PropertyImagesSerializer(instance=obj.property_image.all(), many=True).data

    def create(self, validated_data):
        images = validated_data.pop('images') if 'images' in validated_data and validated_data['images'] else None
        parent = super(PropertySerializer, self).create(validated_data)
        if images:
            serializer = PropertyImagesSerializer(data=[{'image': i, 'property': parent.id} for i in images], many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return parent
