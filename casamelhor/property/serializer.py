from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet
from ..account.serializer import AuthUserSimpleDataSerializer


class ChildAmenitiesAttributeSerializer(serializers.ModelSerializer):
    is_select = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AmenitiesAttribute
        fields = "__all__"


class ChildAmenitiesGroupSerializer(serializers.ModelSerializer):
    attributes = ChildAmenitiesAttributeSerializer(read_only=True, many=True)

    class Meta:
        model = AmenitiesGroup
        fields = ('id', 'name', 'is_active', 'attributes')


class AmenitiesSerializer(serializers.ModelSerializer):
    amenities_group = ChildAmenitiesGroupSerializer(read_only=True, many=True)

    class Meta:
        model = Amenities
        fields = ('id', 'name', 'is_active', 'created_at', 'updated_at', 'amenities_group')


class AmenitiesGroupSerializer(serializers.ModelSerializer):
    amenity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AmenitiesGroup
        fields = ('id', 'name', 'is_active', 'amenity', 'amenity_id', 'amenities_groups_attribute')
        extra_kwargs = {'amenity_id': {'source': 'amenity', 'write_only': True}}

    def get_amenity(self, obj):
        data = AmenitiesSerializer(instance=obj.amenity, many=False).data
        data.pop('amenities_group')
        return data


class AmenitiesAttributeSerializer(serializers.ModelSerializer):
    amenity_group = AmenitiesGroupSerializer(read_only=True)

    class Meta:
        model = AmenitiesAttribute
        fields = ['id', 'name', 'is_active', 'amenity_group', 'amenity_group_id', 'image']
        extra_kwargs = {'amenity_group_id': {'source': 'amenity_group', 'write_only': True}}


class PropertyImagesSerializer(serializers.ModelSerializer):
    image = serializers.FileField(allow_empty_file=True, use_url=False)

    class Meta:
        model = PropertyImages
        fields = "__all__"


class PropertySerializer(serializers.ModelSerializer):
    property_amenities = AmenitiesAttributeSerializer(read_only=True, many=True)
    images = serializers.ListField(child=serializers.FileField(allow_empty_file=True, use_url=False), write_only=True, required=False)
    property_images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'name', 'description', 'house_number', 'building_number', 'area', 'city', 'country', 'state', 'zipcode', 'latitude',
                  'longitude', 'numbers_of_rooms', 'check_in_time', 'check_out_time', 'house_role', 'property_amenities', 'allow_booking_managers',
                  'restrict_booking_managers', 'property_amenities_id', 'created_at', 'updated_at', 'images', 'property_images']
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


class PropertySimpleDataSerializer(serializers.ModelSerializer):
    property_amenities = serializers.SerializerMethodField()
    allow_booking_managers = AuthUserSimpleDataSerializer(read_only=True, many=True)

    class Meta:
        model = Property
        fields = "__all__"

    def get_property_amenities(self, obj):
        return obj.property_amenities.name


class PropertyInactiveReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInactiveReasons
        fields = "__all__"


class PropertySettingsSerializer(serializers.ModelSerializer):
    reason = PropertyInactiveReasonsSerializer(read_only=True)
    property = PropertySimpleDataSerializer(read_only=True)
    property_managers = AuthUserSimpleDataSerializer(read_only=True, many=True)

    class Meta:
        model = PropertySettings
        fields = ["id", "property", "property_managers", "status", 'reason', 'inactive_property_from', 'inactive_property_to', 'email', 'created_at',
                  "updated_at", 'reason_id', 'property_id', 'property_managers_id']
        extra_kwargs = {'reason_id': {'source': 'reason', 'write_only': True}, 'property_id': {'source': 'property', 'write_only': True},
                        'property_managers_id': {'source': 'property_managers', 'write_only': True}}


class PropertyEmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyEmergencyContact
        fields = "__all__"


class RoomsImagesSerializer(serializers.ModelSerializer):
    image = serializers.FileField(allow_empty_file=True, use_url=False)

    class Meta:
        model = RoomsImages
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    room_amenities = AmenitiesAttributeSerializer(read_only=True, many=True)
    property = PropertySimpleDataSerializer(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = ('id', 'property', 'name', 'description', 'numbers_of_beds', 'bed_type', 'preference', 'accommodates', 'room_amenities',
                  'property_id', 'allow_booking_managers', 'restrict_booking_managers', 'room_amenities_id', 'created_at', 'updated_at', 'images')
        extra_kwargs = {'property_id': {'source': 'property', 'write_only': True},
                        'room_amenities_id': {'source': 'room_amenities', 'write_only': True}}

    def get_images(self, obj):
        return RoomsImagesSerializer(instance=obj.property_rooms_image.all(), many=True).data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class GetAmenitiesAttributeSerializer(serializers.ModelSerializer):
    is_select = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AmenitiesAttribute
        fields = "__all__"

    def get_is_select(self, obj):
        return True if obj.id in self.context else False


class GetAmenitiesGroupSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AmenitiesGroup
        fields = ('id', 'name', 'is_active', 'attributes')

    def get_attributes(self, obj):
        data = GetAmenitiesAttributeSerializer(instance=obj.amenities_groups_attribute.all(), many=True, context=self.context).data
        return data


class GetPropertySerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"

    def get_amenities(self, obj):
        ids = [i['id'] for i in obj.property_amenities.filter().values('id')]
        data = GetAmenitiesGroupSerializer(instance=AmenitiesGroup.objects.all(), many=True, context=ids).data
        return data


class GetRoomSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def get_amenities(self, obj):
        ids = [i['id'] for i in obj.room_amenities.filter().values('id')]
        data = GetAmenitiesGroupSerializer(instance=AmenitiesGroup.objects.all(), many=True, context=ids).data
        return data


class SettingsOfPropertySerializer(serializers.ModelSerializer):
    reason = PropertyInactiveReasonsSerializer(read_only=True)

    class Meta:
        model = PropertySettings
        fields = "__all__"
        extra_fields = ['reason']


class GetPropertySettingSerializer(serializers.ModelSerializer):
    property_settings = serializers.SerializerMethodField(read_only=True)
    property_emergency_contact = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"
        extra_fields = ['property_settings', 'property_emergency_contact']

    def get_property_settings(self, obj):
        return SettingsOfPropertySerializer(instance=obj.property_settings.first(), many=False).data

    def get_property_emergency_contact(self, obj):
        return PropertyEmergencyContactSerializer(instance=obj.property_emergency_contact.first(), many=False).data


class RoomsOfPropertySerializer(serializers.ModelSerializer):
    room_amenities = AmenitiesAttributeSerializer(read_only=True, many=True)
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"
        extra_fields = ['room_amenities', 'images']

    def get_images(self, obj):
        return RoomsImagesSerializer(instance=obj.property_rooms_image.all(), many=True).data


class GetPropertyRoomsSerializer(serializers.ModelSerializer):
    property_room = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Property
        fields = "__all__"
        extra_fields = ['property_room', ]

    def get_property_room(self, obj):
        return RoomsOfPropertySerializer(instance=obj.property_room.all(), many=True).data
