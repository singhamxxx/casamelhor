from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework import viewsets, renderers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from ..permissions import IsSuperUser


class PropertyView(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()

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
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (FormParser, MultiPartParser)

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


