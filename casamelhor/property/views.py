from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework import viewsets, renderers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from ..permissions import IsSuperUser
from .forms import PropertyImagesForm


class PropertyView(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Properties Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Delete Successfully", "isSuccess": True, "status": 200})


class PropertyImageView(viewsets.ModelViewSet):
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Images Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Images Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Images Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Images Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Images Delete Successfully", "isSuccess": True, "status": 200})


class PropertyInactiveReasonsView(viewsets.ModelViewSet):
    serializer_class = PropertyInactiveReasonsSerializer
    queryset = PropertyInactiveReasons.objects.all()
    parser_classes = (FormParser,)
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Inactive Reasons Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Inactive Reasons Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Inactive Reasons Delete Successfully", "isSuccess": True, "status": 200})


class PropertySettingsView(viewsets.ModelViewSet):
    serializer_class = PropertySettingsSerializer
    queryset = PropertySettings.objects.all()
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Settings Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Settings Get All Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Settings Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Settings Update Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Settings Delete Successfully", "isSuccess": True, "status": 200})


class PropertyEmergencyContactView(viewsets.ModelViewSet):
    serializer_class = PropertyEmergencyContactSerializer
    queryset = PropertyEmergencyContact.objects.all()
    parser_classes = (FormParser,)
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Emergency Contacts Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Emergency Contact Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Emergency Contact Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Emergency Contact Update Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Emergency Contact Delete Successfully", "isSuccess": True, "status": 200})


class RoomsView(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Rooms Images Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Rooms Images Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        images = None
        if 'images' in request.data and request.data['images']:
            images = request.data.pop('images')
        response_data = super(RoomsView, self).create(request, *args, **kwargs).data
        if images:
            data = [{'room': response_data['id'], 'image': i} for i in images]
            serializer = RoomsImagesSerializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
        serializer = self.get_serializer(Room.objects.get(id=response_data['id']))
        return Response({"data": serializer.data, "message": "Rooms Images Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(RoomsView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Rooms Images Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        response_data = super(RoomsView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Rooms Images Delete Successfully", "isSuccess": True, "status": 200})
