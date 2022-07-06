from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *


@api_view(['GET'])
def amenities_view(request, id=None):
    if id:
        obj, many = Amenities.objects.get(id=id), False
    else:
        obj, many = Amenities.objects.filter().order_by('-created_at'), True
    data = AmenitiesSerializer(obj, many=many).data
    return Response({"data": data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AmenitiesMiddleware)
def create_amenities_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        serializer = AmenitiesSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Create Amenities", "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(AmenitiesMiddleware)
@decorator_from_middleware(TokenAuthenticationMiddleware)
def edit_amenities_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        amenity = Amenities.objects.get(id=id)
        serializer = AmenitiesSerializer(data=form.cleaned_data, instance=amenity, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Edit Amenities", "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['DELETE'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def delete_amenities_view(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        Amenities.objects.get(id=id).delete()
        return Response({"data": None, "message": "Successfully Delete Amenities", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
def amenities_group_view(request, id=None):
    if id:
        obj = AmenitiesGroup.objects.get(id=id)
        many = False
    else:
        obj = AmenitiesGroup.objects.filter().order_by('-created_at')
        many = True
    data = AmenitiesGroupSerializer(obj, many=many).data
    return Response({"data": data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AmenitiesGroupMiddleware)
def create_amenities_group_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        form.cleaned_data['amenity_id'] = form.cleaned_data['amenity'].id
        serializer = AmenitiesGroupSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Create Amenities Group", "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"] if "__all__" in error else {key: error[key] for key in error}
            return Response({"data": None, "message": serializer.errors, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AmenitiesGroupMiddleware)
def edit_amenities_group_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        amenity_group = AmenitiesGroup.objects.get(id=id)
        if 'amenity' in form.cleaned_data and form.cleaned_data['amenity']:
            form.cleaned_data['amenity_id'] = form.cleaned_data['amenity'].id
        serializer = AmenitiesGroupSerializer(data=form.cleaned_data, instance=amenity_group, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Edit Amenities Group", "isSuccess": True, "status": 200}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['DELETE'])
def delete_amenities_group_view(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        AmenitiesGroup.objects.get(id=id).delete()
        return Response({"data": None, "message": "Successfully Delete Amenities Group", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
def amenities_attribute_view(self, request, id=None):
    if id:
        obj = AmenitiesAttribute.objects.get(id=id)
        many = False
    else:
        obj = AmenitiesAttribute.objects.filter().order_by('-created_at')
        many = True
    data = AmenitiesAttributeSerializer(obj, many=many).data
    return Response({"data": data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)
