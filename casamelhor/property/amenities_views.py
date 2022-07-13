from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from ..account.middleware import TokenAuthenticationMiddleware
from .middleware import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin


class AmenitiesView(ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AmenitiesRetrieveView(RetrieveModelMixin, GenericAPIView):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=False)
        return Response({"data": serializer.data, "message": "Successfully Get Amenities", "isSuccess": True, "status": 200}, status=200)


class AmenitiesCreateView(CreateModelMixin, GenericAPIView):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AmenitiesUpdateView(UpdateModelMixin, GenericAPIView):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class AmenitiesDestroyView(DestroyModelMixin, GenericAPIView):
    serializer_class = AmenitiesSerializer
    queryset = Amenities.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
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
@decorator_from_middleware(TokenAuthenticationMiddleware)
def delete_amenities_group_view(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        AmenitiesGroup.objects.get(id=id).delete()
        return Response({"data": None, "message": "Successfully Delete Amenities Group", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
def amenities_attribute_view(request, id=None):
    if id:
        obj = AmenitiesAttribute.objects.get(id=id)
        many = False
    else:
        obj = AmenitiesAttribute.objects.filter().order_by('-created_at')
        many = True
    data = AmenitiesAttributeSerializer(obj, many=many).data
    return Response({"data": data, "message": "Successfully Get Amenities Attribute", "isSuccess": True, "status": 200}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AmenitiesAttributeMiddleware)
def create_amenities_attribute_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        form.cleaned_data['amenity_group_id'] = form.cleaned_data['amenity_group'].id
        serializer = AmenitiesAttributeSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Create Amenities Attribute", "isSuccess": True, "status": 200},
                            status=200)
        else:
            error = serializer.errors
            error = error["__all__"] if "__all__" in error else {key: error[key] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AmenitiesAttributeMiddleware)
def edit_amenities_attribute_view(request, form, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        amenity_attribute = AmenitiesAttribute.objects.get(id=id)
        if 'amenity_group' in form.cleaned_data and form.cleaned_data['amenity_group']:
            form.cleaned_data['amenity_group_id'] = form.cleaned_data['amenity_group'].id
        serializer = AmenitiesAttributeSerializer(data=form.cleaned_data, instance=amenity_attribute, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Successfully Edit Amenities Attribute", "isSuccess": True, "status": 200},
                            status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['DELETE'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def delete_amenities_attribute_view(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        AmenitiesAttribute.objects.get(id=id).delete()
        return Response({"data": None, "message": "Successfully Delete Amenities Attribute", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)
