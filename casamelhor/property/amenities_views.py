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
    permission_classes = (IsSuperUser, )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(AmenitiesView, self).create(request, *args, **kwargs)

        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(AmenitiesView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(AmenitiesView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class AmenitiesGroupView(viewsets.ModelViewSet):
    serializer_class = AmenitiesGroupSerializer
    queryset = AmenitiesGroup.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsSuperUser, )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(AmenitiesGroupView, self).create(request, *args, **kwargs)

        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(AmenitiesGroupView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(AmenitiesGroupView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})


class AmenitiesAttributeView(viewsets.ModelViewSet):
    serializer_class = AmenitiesAttributeSerializer
    queryset = AmenitiesAttribute.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (IsSuperUser, )

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        response_data = super(AmenitiesAttributeView, self).create(request, *args, **kwargs)

        return Response({"data": response_data.data})

    def update(self, request, *args, **kwargs):
        response_data = super(AmenitiesAttributeView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data})

    def destroy(self, request, *args, **kwargs):
        response_data = super(AmenitiesAttributeView, self).destroy(request, *args, **kwargs)
        return Response({"data": response_data.data})
