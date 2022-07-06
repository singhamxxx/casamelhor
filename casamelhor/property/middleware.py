from django.utils.deprecation import MiddlewareMixin
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import os
import sys


class AmenitiesMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        id, instance = None, None
        if request.method == "PUT":
            id = view_kwargs['id']
            instance = AmenitiesGroup.objects.get(id=view_kwargs['id'])
        form = AmenitiesForm(request.data, instance=instance)
        if form.is_valid():
            return view_func(request, form, id)
        else:
            error = form.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


class AmenitiesGroupMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        id, instance = None, None
        if request.method == "PUT":
            id = view_kwargs['id']
            instance = AmenitiesGroup.objects.get(id=view_kwargs['id'])
        form = AmenitiesGroupForm(request.data, instance=instance)
        if form.is_valid():
            return view_func(request, form, id)
        else:
            error = form.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


class AmenitiesAttributeMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            user = request.user if request.user.is_authenticated else None
            form = AmenitiesAttributeForm(request.data, initial=user)
            if form.is_valid():
                return view_func(request, form)
            else:
                error = form.errors
                error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
                return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
