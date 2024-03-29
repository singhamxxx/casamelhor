from .serializer import *
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from ..permissions import IsSuperUser
from rest_framework.response import Response


class AmenitiesView(viewsets.ModelViewSet):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()
    parser_classes = (FormParser, MultiPartParser)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Amenities Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Successfully Get Amenity", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            if not Amenities.objects.filter(name=request.data['name']).exists():
                response_data = super(AmenitiesView, self).create(request, *args, **kwargs)
                return Response({"data": response_data.data, "message": "Successfully Create Amenity", "isSuccess": True, "status": 200})
            else:
                return Response({"data": None, "message": "Amenities Already exists", "isSuccess": True, "status": 200})
        else:
            return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            if self.get_object().name != request.data['name'] and Amenities.objects.filter(name=request.data['name']).exists():
                return Response({"data": None, "message": "Amenities Already exists", "isSuccess": True, "status": 200})
            response_data = super(AmenitiesView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully edit Amenity", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            super(AmenitiesView, self).destroy(request, *args, **kwargs)
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "Successfully delete Amenity", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)


class AmenitiesGroupView(viewsets.ModelViewSet):
    serializer_class = AmenitiesGroupSerializer
    queryset = AmenitiesGroup.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes_by_action = [IsSuperUser, ]

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
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesGroupView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Update Amenities Group", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            super(AmenitiesGroupView, self).destroy(request, *args, **kwargs)
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "Successfully Delete Amenities Group", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)


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
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(AmenitiesAttributeView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Successfully Edit Amenities Attribute", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            super(AmenitiesAttributeView, self).destroy(request, *args, **kwargs)
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "Successfully Delete Amenities Attribute", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)
