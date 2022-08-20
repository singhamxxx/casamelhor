from django.urls import path
from .amenities_views import *
from .views import *

urlpatterns = [
    # Amenities urls
    path('amenities/get/', AmenitiesView.as_view({'get': 'list'})),
    path('amenities/get/<int:pk>/', AmenitiesView.as_view({'get': 'retrieve'})),
    path('amenities/create/', AmenitiesView.as_view({'post': 'create'})),
    path('amenities/edit/<int:pk>/', AmenitiesView.as_view({'put': 'update'})),
    path('amenities/delete/<int:pk>/', AmenitiesView.as_view({'delete': 'destroy'})),

    # amenities groups urls
    path('amenities/groups/get/', AmenitiesGroupView.as_view({'get': 'list'})),
    path('amenities/group/get/<int:pk>/', AmenitiesGroupView.as_view({'get': 'retrieve'})),
    path('amenities/group/create/', AmenitiesGroupView.as_view({'post': 'create'})),
    path('amenities/group/edit/<int:pk>/', AmenitiesGroupView.as_view({'put': 'update'})),
    path('amenities/group/delete/<int:pk>/', AmenitiesGroupView.as_view({'delete': 'destroy'})),

    # amenities attribute urls
    path('amenities/attribute/get/', AmenitiesAttributeView.as_view({'get': 'list'})),
    path('amenities/attributes/get/<int:pk>/', AmenitiesAttributeView.as_view({'get': 'retrieve'})),
    path('amenities/attribute/create/', AmenitiesAttributeView.as_view({'post': 'create'})),
    path('amenities/attribute/edit/<int:pk>/', AmenitiesAttributeView.as_view({'put': 'update'})),
    path('amenities/attribute/delete/<int:pk>/', AmenitiesAttributeView.as_view({'delete': 'destroy'})),

    # Property urls
    path('create/', PropertyView.as_view({'post': 'create'}), name='property_create'),
    path('get/', PropertyView.as_view({'get': 'list'}), name='property_get'),
    path('get/<int:pk>/', PropertyView.as_view({'get': 'retrieve'}), name='property_get_one'),
    path('edit/<int:pk>/', PropertyView.as_view({'put': 'update'}), name='property_edit_one'),
    path('delete/<int:pk>/', PropertyView.as_view({'delete': 'destroy'}), name='property_destroy_one'),

    # Property Image urls
    path('image/create/', PropertyImageView.as_view({'post': 'create'}), name='property_image_create'),
    path('images/get/', PropertyImageView.as_view({'get': 'list'}), name='property_image_get'),
    path('image/get/<int:pk>/', PropertyImageView.as_view({'get': 'retrieve'}), name='property_image_get_one'),
    path('image/edit/<int:pk>/', PropertyImageView.as_view({'put': 'update'}), name='property_image_edit_one'),
    path('image/delete/<int:pk>/', PropertyImageView.as_view({'delete': 'destroy'}), name='property_image_destroy_one'),

    # Property Settings urls
    path('setting/create/', PropertySettingsView.as_view({'post': 'create'}), name='property_setting_create'),
    path('settings/get/', PropertySettingsView.as_view({'get': 'list'}), name='property_setting_get'),
    path('setting/get/<int:pk>/', PropertySettingsView.as_view({'get': 'retrieve'}), name='property_setting_get_one'),
    path('setting/edit/<int:pk>/', PropertySettingsView.as_view({'put': 'update'}), name='property_setting_edit_one'),
    path('setting/delete/<int:pk>/', PropertySettingsView.as_view({'delete': 'destroy'}), name='property_setting_destroy_one'),

    # Property Inactive Reasons urls
    path('inactive/reason/create/', PropertyInactiveReasonsView.as_view({'post': 'create'}), name='property_inactive_reasons_create'),
    path('inactive/reasons/get/', PropertyInactiveReasonsView.as_view({'get': 'list'}), name='property_inactive_reasons_get'),
    path('inactive/reason/get/<int:pk>/', PropertyInactiveReasonsView.as_view({'get': 'retrieve'}), name='property_inactive_reasons_get_one'),
    path('inactive/reason/edit/<int:pk>/', PropertyInactiveReasonsView.as_view({'put': 'update'}), name='property_inactive_reasons_edit_one'),
    path('inactive/reason/delete/<int:pk>/', PropertyInactiveReasonsView.as_view({'delete': 'destroy'}), name='property_inactive_reasons_destroy_one'),

    # Property Rooms urls
    path('room/create/', RoomsView.as_view({'post': 'create'}), name='room_create'),
    path('rooms/get/', RoomsView.as_view({'get': 'list'}), name='property_setting_get'),
    path('room/get/<int:pk>/', RoomsView.as_view({'get': 'retrieve'}), name='property_setting_get_one'),
    path('room/edit/<int:pk>/', RoomsView.as_view({'put': 'update'}), name='property_setting_edit_one'),
    path('room/delete/<int:pk>/', RoomsView.as_view({'delete': 'destroy'}), name='property_setting_destroy_one'),

]
