from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework import generics


@api_view(['GET'])
def property_view(request, id=None):
    if id:
        obj, many = Property.objects.get(id=id), False
    else:
        obj, many = Property.objects.filter().order_by('-created_at'), True
    data = PropertySerializer(obj, many=many).data
    return Response({"data": data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
@decorator_from_middleware(PropertyMiddleware)
def create_property_view(request, form, id=None):
    form.cleaned_data['property_amenities_id'] = form.cleaned_data['property_amenities'].id
    serializer = PropertySerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data, "message": "Successfully Create property", "isSuccess": True, "status": 200}, status=200)
    else:
        error = serializer.errors
        error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(PropertyMiddleware)
def edit_property_view(request, form, id=None):
    property = Property.objects.get(id=id)
    serializer = PropertySerializer(data=form.cleaned_data, instance=property, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data, "message": "Successfully Edit Amenities", "isSuccess": True, "status": 200}, status=200)
    else:
        error = serializer.errors
        error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
