from django.urls import path
from .amenities_views import *
from .views import *

urlpatterns = [
    path('amenities/get/', AmenitiesView.as_view({'get': 'list'})),
    path('amenities/get/<int:pk>/', AmenitiesView.as_view({'get': 'retrieve'})),
    path('amenities/create/', AmenitiesView.as_view({'post': 'create'})),
    path('amenities/edit/<int:pk>/', AmenitiesView.as_view({'put': 'update'})),
    path('amenities/delete/<int:pk>/', AmenitiesView.as_view({'delete': 'destroy'})),

    path('amenities/group/get/', AmenitiesGroupView.as_view({'get': 'list'})),
    path('amenities/group/get/<int:pk>/', AmenitiesGroupView.as_view({'get': 'retrieve'})),
    path('amenities/group/create/', AmenitiesGroupView.as_view({'post': 'create'})),
    path('amenities/group/edit/<int:pk>/', AmenitiesGroupView.as_view({'put': 'update'})),
    path('amenities/group/delete/<int:pk>/', AmenitiesGroupView.as_view({'delete': 'destroy'})),

    path('amenities/attribute/get/', AmenitiesAttributeView.as_view({'get': 'list'})),
    path('amenities/attribute/get/<int:pk>/', AmenitiesAttributeView.as_view({'get': 'retrieve'})),
    path('amenities/attribute/create/', AmenitiesAttributeView.as_view({'post': 'create'})),
    path('amenities/attribute/edit/<int:pk>/', AmenitiesAttributeView.as_view({'put': 'update'})),
    path('amenities/attribute/delete/<int:pk>/', AmenitiesAttributeView.as_view({'delete': 'destroy'})),

    path('create/', PropertyView.as_view({'post': 'create'}), name='property_create'),
    path('get/', PropertyView.as_view({'get': 'list'}), name='property_get'),
    path('get/<int:pk>/', PropertyView.as_view({'get': 'retrieve'}), name='property_get_one'),
    path('edit/<int:pk>/', PropertyView.as_view({'put': 'update'}), name='property_edit_one'),
    path('delete/<int:pk>/', PropertyView.as_view({'delete': 'destroy'}), name='property_destroy_one'),

    path('image/create/', PropertyImageView.as_view({'post': 'create'}), name='property_image_create'),
    path('image/get/', PropertyImageView.as_view({'get': 'list'}), name='property_image_get'),
    path('image/get/<int:pk>/', PropertyImageView.as_view({'get': 'retrieve'}), name='property_image_get_one'),
    path('image/edit/<int:pk>/', PropertyImageView.as_view({'put': 'update'}), name='property_image_edit_one'),
    path('image/delete/<int:pk>/', PropertyImageView.as_view({'delete': 'destroy'}), name='property_image_destroy_one'),

]
