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
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class PropertyImageView(viewsets.ModelViewSet):
    serializer_class = PropertyImagesSerializer
    queryset = PropertyImages.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyImageView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class PropertyInactiveReasonsView(viewsets.ModelViewSet):
    serializer_class = PropertyInactiveReasonsSerializer
    queryset = PropertyInactiveReasons.objects.all()
    parser_classes = (FormParser,)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyInactiveReasonsView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class PropertySettingsView(viewsets.ModelViewSet):
    serializer_class = PropertySettingsSerializer
    queryset = PropertySettings.objects.all()
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertySettingsView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class PropertyEmergencyContactView(viewsets.ModelViewSet):
    serializer_class = PropertyEmergencyContactSerializer
    queryset = PropertyEmergencyContact.objects.all()
    parser_classes = (FormParser,)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(PropertyEmergencyContactView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class RoomsImagesView(viewsets.ModelViewSet):
    serializer_class = RoomsImagesSerializer
    queryset = RoomsImages.objects.all()
    parser_classes = (FormParser,)
    permission_classes_by_action = {'create': [IsSuperUser], 'update': [IsSuperUser], 'destroy': [IsSuperUser]}

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(RoomsImagesView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(RoomsImagesView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(RoomsImagesView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})
