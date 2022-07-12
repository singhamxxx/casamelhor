from django.urls import path
from .amenities_views import *
from .views import *

urlpatterns = [
    path('amenities/get/', AmenitiesListView.as_view(), name='amenities_get'),
    path('amenities/get/<int:pk>/', AmenitiesRetrieveView.as_view(), name='amenities_get_one'),
    path('amenities/create/', AmenitiesCreateView.as_view(), name='amenities_create'),
    path('amenities/edit/<int:pk>/', AmenitiesUpdateView.as_view(), name='amenities_edit'),
    path('amenities/delete/<int:pk>/', AmenitiesDestroyView.as_view(), name='amenities_delete'),

    path('amenities/group/get/', amenities_group_view, name='amenities_group_get'),
    path('amenities/group/get/<int:id>/', amenities_group_view, name='amenities_group_get_one'),
    path('amenities/group/create/', create_amenities_group_view, name='amenities_group_create'),
    path('amenities/group/edit/<int:id>/', edit_amenities_group_view, name='amenities_group_edit'),
    path('amenities/group/delete/<int:id>/', delete_amenities_group_view, name='amenities_group_delete'),

    path('amenities/attribute/get/', amenities_attribute_view, name='amenities_attribute_get'),
    path('amenities/attribute/get/<int:id>/', amenities_attribute_view, name='amenities_attribute_get'),
    path('amenities/attribute/create/', create_amenities_attribute_view, name='amenities_attribute_create'),
    path('amenities/attribute/edit/<int:id>/', edit_amenities_attribute_view, name='amenities_attribute_edit'),
    path('amenities/attribute/delete/<int:id>/', delete_amenities_attribute_view, name='amenities_attribute_delete'),

    path('create/', create_property_view, name='property_create'),
    path('get/', property_view, name='property_get'),
    path('get/<int:id>/', property_view, name='property_get_one'),
    path('edit/<int:id>/', edit_property_view, name='property_edit_one'),
]
