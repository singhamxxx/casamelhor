from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from ..permissions import IsSuperUser


class AmenitiesView(viewsets.ModelViewSet):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()
    parser_classes = (FormParser, MultiPartParser)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Successfully Get Amenity", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesView, self).create(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Create Amenity", "isSuccess": True, "status": 200})
        else:
            return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully edit Amenity", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesView, self).destroy(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully delete Amenity", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)


class AmenitiesGroupView(viewsets.ModelViewSet):
    serializer_class = AmenitiesGroupSerializer
    queryset = AmenitiesGroup.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Successfully Get Amenities Groups", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Successfully Get Amenities Group", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesGroupView, self).create(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Create Amenities Group", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesGroupView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Update Amenities Group", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesGroupView, self).destroy(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Delete Amenities Group", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)


class AmenitiesAttributeView(viewsets.ModelViewSet):
    serializer_class = AmenitiesAttributeSerializer
    queryset = AmenitiesAttribute.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Successfully Get Amenities Attribute", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Successfully Get Amenities Attribute", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesAttributeView, self).create(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Create Amenities Attribute", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesAttributeView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Edit Amenities Attribute", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesAttributeView, self).destroy(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Delete Amenities Attribute", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 403}, status=200)
