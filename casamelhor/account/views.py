from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from rest_framework.response import Response
from .emails import _send_account_confirmation_email
from .serializer import *
from django.contrib.auth.tokens import default_token_generator
from .middleware import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
@decorator_from_middleware(RegisterMiddleware)
def registration_view(request, form):
    form.cleaned_data["login_ip"] = get_client_ip(request)
    form.cleaned_data['role'] = form.cleaned_data['role'].id
    serializer = AuthUserSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        user = User.objects.get(email=data['email'])
        user.save()
        token = default_token_generator.make_token(user)
        url = f"http://192.168.29.72:8000/api/v1/account/user/email/verify/?token={token}&email={user.email}"
        _send_account_confirmation_email(user, url)
        return Response({"data": data, "message": "User Successfully Created", "isSuccess": True, "status": 200}, status=200)
    else:
        error = serializer.errors
        error = error["__all__"][0] if "__all__" in error else "".join(key + f" {error[key][0]}\n" for key in error)
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    phone_or_email = form.cleaned_data['phone_or_email']
    password = form.cleaned_data['password']
    user_obj = User.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email)).first()
    if user_obj.check_password(password):
        if user_obj.is_email:
            serializer = TokenObtainPairSerializer(data={'email': user_obj.email, 'password': password})
            token = serializer.validate({'email': user_obj.email, 'password': password})
            user_obj.last_login = datetime.now()
            user_obj.login_ip = get_client_ip(request)
            user_obj.save()
            serializer = AuthUserSerializer(instance=user_obj, many=False).data
            serializer["token"] = token['access']
            data = {'data': serializer, "message": "Successfully Login", "isSuccess": True, "status": 200}
            return Response(data, status=200)
        return Response(
            {"data": {'email': user_obj.email, 'is_email': user_obj.is_email}, "message": "Email not verified",
             "isSuccess": False,
             "status": 200}, status=200)
    else:
        return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['GET'])
def email_verification_view(request):
    token = request.GET.get('token')
    email = request.GET.get('email')
    user = User.objects.filter(email=email)
    if user.exists():
        if not user.first().is_email:
            if default_token_generator.check_token(user.first(), token):
                user.update(is_email=True, updated_at=datetime.now())
                return Response({"data": None, "message": "Successfully verified", "isSuccess": True, "status": 200},
                                status=200)
            return Response({"data": None, "message": "Invalid Token", "isSuccess": False, "status": 400}, status=200)
        return Response({"data": None, "message": "Email Already verified", "isSuccess": False, "status": 200}, status=200)
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 404}, status=200)


@api_view(['POST'])
def resend_email_view(request):
    phone_or_email = request.POST.get('phone_or_email')
    user = User.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email))
    if user.exists():
        token = default_token_generator.make_token(user.first())
        url = f"http://192.168.29.72:8000/api/v1/account/user/email/verify/?token={token}&email={user.first().email}"
        _send_account_confirmation_email(user.first(), url)
        return Response({"data": None, "message": "Successfully email send", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 400}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_password_change_view(request):
    if request.user.is_authenticated:
        if request.user.check_password(request.POST.get('old_password')):
            request.user.set_password(request.POST.get('password'))
            request.user.save()
            return Response(
                {"data": None, "isSuccess": True, "message": "Successfully password changed", "status": 200},
                status=200)
        return Response({"data": None, "isSuccess": True, "message": "Incorrect password", "status": 200}, status=200)
    return Response({"data": None, "message": "Permission Denied", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
def user_forgot_password_email_send_view(request):
    phone_or_email = request.POST.get('phone_or_email')
    user = User.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email))
    if user.exists():
        if user.first().is_email and user.first().is_phone:
            token = default_token_generator.make_token(user.first())
            url = f"http://192.168.29.72:8000/api/v1/account/user/forgot-password/verify/?token={token}&email={user.first().email}"
            _send_account_confirmation_email(user.first(), url)
            return Response({"data": None, "message": "Successfully email send", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "Email or phone is not verified", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 400}, status=200)


@api_view(['POST'])
def user_forgot_password_view(request):
    token = request.GET.get('token')
    email = request.GET.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        if user.is_email and user.is_phone:
            if default_token_generator.check_token(user, token):
                user.set_password(request.POST.get('password'))
                user.save()
                return Response({"data": None, "message": "Successfully changed password", "isSuccess": True, "status": 200}, status=200)
            return Response({"data": None, "message": "Invalid Token", "isSuccess": False, "status": 400}, status=200)
        return Response({"data": None, "message": "Email or phone is not verified", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 400}, status=200)

