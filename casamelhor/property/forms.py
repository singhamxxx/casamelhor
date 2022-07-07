from django import forms
from .models import *


class AmenitiesForm(forms.ModelForm):

    class Meta:
        model = Amenities
        fields = '__all__'


class AmenitiesGroupForm(forms.ModelForm):

    class Meta:
        model = AmenitiesGroup
        fields = "__all__"


class AmenitiesAttributeForm(forms.ModelForm):

    class Meta:
        model = AmenitiesAttribute
        fields = '__all__'


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = '__all__'
