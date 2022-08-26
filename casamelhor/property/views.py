from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework import viewsets, renderers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from ..permissions import IsSuperUser, IsAuthenticated, IsBookingUser, IsCasamelhorPropertyManagerUser
from .forms import PropertyImagesForm


class PropertySearchView(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [IsSuperUser, IsCasamelhorPropertyManagerUser]


class PropertyView(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Properties Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = GetPropertySerializer(instance=self.get_object(), many=False)
        return Response({"data": serializer.data, "message": "Property Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(PropertyView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Property Delete Successfully", "isSuccess": True, "status": 200})


class PropertyImageView(viewsets.ModelViewSet):
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Images Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Images Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        property_id = request.data['property_id']
        data = [{'property': property_id, 'image': i} for i in request.FILES.getlist('images')]
        response_data = self.get_serializer(data=data, many=True)
        response_data.is_valid(raise_exception=True)
        response_data.save()
        return Response({"data": response_data.data, "message": "Property Images Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Images Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(PropertyImageView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Property Images Delete Successfully", "isSuccess": True, "status": 200})


class PropertyInactiveReasonsView(viewsets.ModelViewSet):
    serializer_class = PropertyInactiveReasonsSerializer
    queryset = PropertyInactiveReasons.objects.all()
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
        super(PropertyInactiveReasonsView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Property Inactive Reasons Delete Successfully", "isSuccess": True, "status": 200})


class PropertySettingsView(viewsets.ModelViewSet):
    serializer_class = PropertySettingsSerializer
    queryset = PropertySettings.objects.all()
    permission_classes = [IsSuperUser, ]

    def retrieve(self, request, *args, **kwargs):
        serializer = GetPropertySettingSerializer(instance=Property.objects.get(id=kwargs['pk']), many=False)
        return Response({"data": serializer.data, "message": "Property Settings Get All Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        data = request.data['property_emergency_contact']
        response_data = self.get_serializer(data=request.data['property_settings'])
        response_data.is_valid(raise_exception=True)
        response_data.save()
        serializer = PropertyEmergencyContactSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {"property_emergency_contact": serializer.data, "property_settings": response_data.data}
        return Response({"data": response, "message": "Property Settings Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        data = request.data['property_emergency_contact']
        obj = PropertyEmergencyContact.objects.get(id=request.data['property_emergency_contact_id'])
        response_data = self.get_serializer(data=request.data['property_settings'], instance=self.get_object(), partial=True)
        response_data.is_valid(raise_exception=True)
        response_data.save()
        serializer = PropertyEmergencyContactSerializer(data=data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {"property_emergency_contact": serializer.data, "property_settings": response_data.data}
        return Response({"data": response, "message": "Property Settings Update Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(PropertySettingsView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Property Settings Delete Successfully", "isSuccess": True, "status": 200})


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
        super(RoomsView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Rooms Images Delete Successfully", "isSuccess": True, "status": 200})


class PropertyRoomsView(viewsets.ModelViewSet):
    serializer_class = GetPropertyRoomsSerializer
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Rooms Images Get Successfully", "isSuccess": True, "status": 200})


class BookingView(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsBookingUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        request.data['booked_by'] = request.user.id
        response_data = super(BookingView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Inactive Reasons Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(BookingView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Property Inactive Reasons Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(BookingView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Property Inactive Reasons Delete Successfully", "isSuccess": True, "status": 200})
