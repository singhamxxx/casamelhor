from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", 'property', 'name', 'description', 'numbers_of_beds', 'bed_type', 'preference', 'accommodates',
                    'created_at', 'updated_at']
    search_fields = ["name", "property__name"]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(Amenities)
admin.site.register(AmenitiesGroup)
admin.site.register(AmenitiesAttribute)
admin.site.register(Property)
admin.site.register(PropertyImages)
admin.site.register(PropertyInactiveReasons)
admin.site.register(PropertySettings)
admin.site.register(PropertyEmergencyContact)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomsImages)
