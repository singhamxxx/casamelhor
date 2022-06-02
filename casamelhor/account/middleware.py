from django.utils.deprecation import MiddlewareMixin
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import os
import sys


class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            jwt_object = JWTAuthentication()
            header = jwt_object.get_header(request)
            if header is not None:
                raw_token = jwt_object.get_raw_token(header)
                validated_token = jwt_object.get_validated_token(raw_token)
                request.user = jwt_object.get_user(validated_token)
                return None
            return None
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return JsonResponse({'data': None, "message": f"{e}, {f_name}, {exc_tb.tb_lineno}", "status": 500},
                                status=200)


class RegisterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            user = request.user if request.user.is_authenticated else None
            form = RegisterForm(request.data, request.FILES, initial=user)
            if form.is_valid():
                return view_func(request, form)
            else:
                error = form.errors
                error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


class UserLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method == "POST":
            form = UserLoginForm(data=request.data)
            if form.is_valid():
                return view_func(request, form)
            else:
                error = form.errors
                error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
                return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
