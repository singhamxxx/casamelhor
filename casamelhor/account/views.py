from rest_framework.decorators import api_view
from django.utils.decorators import decorator_from_middleware
from django.contrib.auth.models import Group, Permission
from .emails import _send_account_confirmation_email
from .serializer import *
from django.contrib.auth.tokens import default_token_generator
from .middleware import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from random import randint

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')


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
    if 'user_permissions' in form.cleaned_data and form.cleaned_data['user_permissions']:
        form.cleaned_data['user_permissions'] = [i.id for i in form.cleaned_data['user_permissions']]
    groups = [form.cleaned_data['role'].id]
    if 'groups' in form.cleaned_data and form.cleaned_data['groups']:
        groups = groups.extend([i.id for i in form.cleaned_data['groups']])
    form.cleaned_data['groups'] = groups
    form.cleaned_data['role_id'] = form.cleaned_data['role'].id
    serializer = AuthUserSerializer(data=form.cleaned_data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return Response({"data": data, "message": "User Successfully Created", "isSuccess": True, "status": 200}, status=200)
    else:
        error = serializer.errors
        error = error["__all__"] if "__all__" in error else {key: error[key] for key in error}
        return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(UserLoginMiddleware)
def user_login_view(request, form):
    phone_or_email = form.cleaned_data['phone_or_email']
    password = form.cleaned_data['password']
    user_obj = User.objects.filter(Q(email=phone_or_email) | Q(phone=phone_or_email)).first()
    if user_obj.check_password(password):
        if not user_obj.is_email:
            otp = randint(10 ** (6 - 1), (10 ** 6) - 1)
            user_obj.email_otp = otp
            user_obj.save()
            _send_account_confirmation_email(user_obj, otp=otp)
            data = {'data': {'email': user_obj.email, 'is_email': user_obj.is_email},
                    "message": "Verification mail sent  on your mail, please verify",
                    "isSuccess": True, "status": 200}
        else:
            serializer = TokenObtainPairSerializer(data={'email': user_obj.email, 'password': password})
            token = serializer.validate({'email': user_obj.email, 'password': password})
            user_obj.last_login = datetime.now()
            user_obj.login_ip = get_client_ip(request)
            user_obj.save()
            serializer = AuthUserSerializer(instance=user_obj, many=False).data
            serializer["token"] = token['access']
            data = {'data': serializer, "message": "Successfully Login", "isSuccess": True, "status": 200}
        return Response(data, status=200)

    else:
        return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
@decorator_from_middleware(UserEmailVerificationMiddleware)
def email_verification_view(request, form):
    otp = form.cleaned_data['otp']
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    user = User.objects.filter(email=email).first()
    if user.check_password(password):
        if user.is_email:
            return Response({"data": None, "message": "Email Already Verified", "isSuccess": True, "status": 200}, status=200)
        if not user.email_otp:
            return Response({"data": None, "message": "Please Resend Email otp", "isSuccess": True, "status": 200}, status=200)
        if user.email_otp == otp:
            serializer = TokenObtainPairSerializer(data={'email': user.email, 'password': password})
            token = serializer.validate({'email': user.email, 'password': password})
            user.last_login = datetime.now()
            user.login_ip = get_client_ip(request)
            user.email_otp = None
            user.is_email = True
            user.updated_at = datetime.now()
            user.save()
            serializer = AuthUserSerializer(instance=user, many=False).data
            serializer["token"] = token['access']
            return Response({'data': serializer, "message": "Successfully Login", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Invalid OTP", "isSuccess": False, "status": 400}, status=200)
    return Response({"data": None, "message": "Password Incorrect", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
def resend_email_otp_view(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        if not user.is_email:
            otp = randint(10 ** (6 - 1), (10 ** 6) - 1)
            user.email_otp = otp
            user.save()
            _send_account_confirmation_email(user, otp=otp)
            return Response({"data": None, "message": "Successfully email send", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "Email Already Verified", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 400}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_password_change_view(request):
    if request.user.is_authenticated:
        if request.POST.get('phone'):
            request.user.phone = request.POST.get('phone')
        if request.user.check_password(request.POST.get('old_password')):
            request.user.set_password(request.POST.get('password'))
            request.user.save()
            return Response({"data": None, "isSuccess": True, "message": "Successfully password changed", "status": 200}, status=200)
        return Response({"data": None, "isSuccess": True, "message": "Incorrect password", "status": 200}, status=200)
    return Response({"data": None, "message": "Permission Denied", "isSuccess": False, "status": 500}, status=200)


@api_view(['POST'])
def user_forgot_password_email_send_view(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email)
    if user.exists():
        if user.first().is_email and user.first().is_phone:
            token = default_token_generator.make_token(user.first())
            url = f"https://casamelhor.onrender.com/api/v1/account/user/forgot-password/verify/?token={token}&email={user.first().email}"
            _send_account_confirmation_email(user.first(), url=url)
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
    return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 404}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_group_of_permissions_view(request, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        many = True
        if id:
            if Group.objects.filter(id=id).exists():
                obj = Group.objects.filter(id=id)
                many = False
            else:
                return Response({"data": None, "message": "Permission`s Group not found", "isSuccess": False, "status": 404}, status=200)
        else:
            obj = Group.objects.filter()
        serializer = AuthUserGroupOFPermissionsSerializer(instance=obj, many=many).data
        return Response({"data": serializer, "message": "Roles Permission`s Group", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_update_profile_view(request):
    if request.user.is_authenticated:
        if 'first_name' in request.POST and request.POST['first_name']:
            request.user.first_name = request.POST['first_name']
        if 'employee_id' in request.POST and request.POST['employee_id']:
            request.user.employee_id = request.POST['employee_id']
        if 'department' in request.POST and request.POST['department']:
            request.user.department = request.POST['department']
        if 'image' in request.FILES and request.FILES['image']:
            image = request.FILES['image']
            request.user.image.save(image.name, image)
        request.user.save()
        serializer = AuthUserSerializer(instance=request.user, many=False).data
        return Response({"data": serializer, "message": "Successfully profile update", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 400}, status=200)


@api_view(['GET'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
def user_permission_view(request, id=None):
    if request.user.is_authenticated and request.user.is_superuser:
        many = True
        if id:
            if Permission.objects.filter(id=id).exists():
                obj = Permission.objects.filter(id=id)
                many = False
            else:
                return Response({"data": None, "message": "Permission not found", "isSuccess": False, "status": 404}, status=200)
        else:
            obj = Permission.objects.filter()
        serializer = AuthUserPermissionsSerializer(instance=obj, many=many).data
        return Response({"data": serializer, "message": "Roles Permissions", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized Use", "isSuccess": False, "status": 400}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AuthUserGroupOFPermissionsMiddleware)
def create_user_group_of_permissions_view(request, form):
    if request.user.is_authenticated and request.user.is_superuser:
        group, created = Group.objects.get_or_create(name=form.cleaned_data['name'])
        group.permissions.set(form.cleaned_data['permissions'])
        serializer = AuthUserGroupOFPermissionsSerializer(instance=group).data
        return Response({"data": serializer, "message": "Roles Permissions", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized Use", "isSuccess": False, "status": 400}, status=200)


@api_view(['PUT'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(AuthUserGroupOFPermissionsMiddleware)
def edit_user_group_of_permissions_view(request, id, form):
    if request.user.is_authenticated and request.user.is_superuser:
        group = Group.objects.get(id=id)
        if group.name != form.cleaned_data['name']:
            group.name = form.cleaned_data['name']
            group.save()
        group.permissions.set(form.cleaned_data['permissions'])
        serializer = AuthUserGroupOFPermissionsSerializer(instance=group).data
        return Response({"data": serializer, "message": "Roles Permissions", "isSuccess": True, "status": 200}, status=200)
    return Response({"data": None, "message": "Unauthorized Use", "isSuccess": False, "status": 400}, status=200)


@api_view(['POST'])
@decorator_from_middleware(TokenAuthenticationMiddleware)
@decorator_from_middleware(VaultMiddleware)
def create_user_vault_view(request, form):
    if request.user.is_authenticated:
        form.cleaned_data['user'] = request.user.id
        serializer = VaultSerializer(data=form.cleaned_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Unauthorized Use", "isSuccess": False, "status": 400}, status=200)
        else:
            error = serializer.errors
            error = error["__all__"][0] if "__all__" in error else {key: error[key][0] for key in error}
            return Response({"data": None, "message": error, "isSuccess": False, "status": 500}, status=200)
    return Response({"data": None, "message": "Unauthorized Use", "isSuccess": False, "status": 400}, status=200)
