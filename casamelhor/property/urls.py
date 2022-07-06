from django.urls import path
from .views import *

urlpatterns = [
    path('amenities/get/', amenities_view, name='amenities_get'),
    path('amenities/get/<int:id>/', amenities_view, name='amenities_get_one'),
    path('amenities/create/', create_amenities_view, name='amenities_create'),
    path('amenities/edit/<int:id>/', edit_amenities_view, name='amenities_edit'),
    path('amenities/delete/<int:id>/', delete_amenities_view, name='amenities_delete'),

    path('amenities/group/get/', amenities_group_view, name='amenities_group_get'),
    path('amenities/group/get/<int:id>/', amenities_group_view, name='amenities_group_get_one'),
    path('amenities/group/create/', create_amenities_group_view, name='amenities_group_create'),
    path('amenities/group/edit/<int:id>/', edit_amenities_group_view, name='amenities_group_edit'),
    path('amenities/group/delete/<int:id>/', delete_amenities_group_view, name='amenities_group_delete'),

    path('amenities/attribute/get/', amenities_attribute_view, name='amenities_attribute_get'),
    path('amenities/attribute/get/<int:id>/', amenities_attribute_view, name='amenities_attribute_get'),
]
