from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from ..account.models import User


class Amenities(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AmenitiesGroup(models.Model):
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE, related_name="amenities_group")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AmenitiesAttribute(models.Model):
    amenity_group = models.ForeignKey(AmenitiesGroup, on_delete=models.CASCADE, related_name="amenities_groups_attribute")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    image = models.FileField(upload_to='amenities_attribute/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=65500, null=True, blank=True)
    house_number = models.CharField(max_length=255, null=True, blank=True)
    building_number = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    numbers_of_rooms = models.IntegerField(null=True, blank=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    house_role = models.TextField(max_length=65500, null=True, blank=True)
    property_amenities = models.ForeignKey(AmenitiesAttribute, on_delete=models.SET_NULL, null=True, related_name="property_amenities")
    allow_booking_managers = models.ManyToManyField(User, related_name="property_allow_booking_manager", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_image")
    image = VersatileImageField(upload_to="property/", ppoi_field='ppoi')
    ppoi = PPOIField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property.name


class PropertyInactiveReasons(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_reasons")
    reason = models.TextField(max_length=65500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason


status_choices = (('Active', 'Active'), ('Inactive', 'Inactive'))


class PropertySettings(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_settings")
    property_managers = models.ManyToManyField(User, related_name="property_managers")
    status = models.CharField(max_length=255, choices=status_choices)
    reason = models.ForeignKey(PropertyInactiveReasons, on_delete=models.SET_NULL, null=True, related_name="property_inactive_reason", blank=True)
    inactive_property_from = models.DateField(null=True, blank=True)
    inactive_property_to = models.DateField(null=True, blank=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status


class PropertyEmergencyContact(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_emergency_contact")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


bed_types_choice = (('Single', 'Single'), ('Queen', 'Queen'), ('Double', 'Double'))
preference_choice = (('Female', 'Female'), ('Male', 'Male'), ('None', 'None'))


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_room")
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=65500)
    numbers_of_beds = models.IntegerField()
    bed_type = models.CharField(max_length=255, choices=bed_types_choice)
    preference = models.CharField(max_length=255, choices=preference_choice)
    accommodates = models.IntegerField()
    room_amenities = models.ForeignKey(AmenitiesAttribute, on_delete=models.SET_NULL, null=True, related_name="room_amenities")
    allow_booking_managers = models.ManyToManyField(User, related_name="room_allow_booking_manager")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RoomsImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="property_rooms_image")
    image = VersatileImageField(upload_to="property/room/", ppoi_field='ppoi')
    ppoi = PPOIField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.url
