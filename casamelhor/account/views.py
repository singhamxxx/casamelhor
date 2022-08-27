from .emails import _send_account_confirmation_email
from .serializer import *
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from django.db.models import Q
from random import randint
from rest_framework import viewsets
from rest_framework_swagger.views import get_swagger_view
from ..permissions import IsSuperUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
schema_view = get_swagger_view(title='Pastebin API')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RegistrationView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()
    permission_classes_by_action = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "All Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Property Inactive Reasons Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            request.data["login_ip"] = get_client_ip(request)
            if 'user_permissions' in request.data and request.data['user_permissions']:
                request.data['user_permissions'] = [i.id for i in request.data['user_permissions']]
            groups = [request.data['role']]
            if 'groups' in request.data and request.data['groups']:
                groups = groups.extend([i.id for i in request.data['groups']])
            request.data['groups'] = groups
            request.data['role_id'] = request.data['role']
            request.data['company_id'] = request.data['company']
            response_data = super(RegistrationView, self).create(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "User Successfully Created", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def update(self, request, *args, **kwargs):
        response_data = super(RegistrationView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "User Successfully Update", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            super(RegistrationView, self).destroy(request, *args, **kwargs)
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "User Delete Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)


class LoginView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):

        phone_or_email = request.data['phone_or_email']
        password = request.data['password']
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


class EmailVerificationView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        otp = int(request.data['otp'])
        email = request.data['email']
        password = request.data['password']
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


class ResendEmailOtpView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
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


class UserPasswordChangeView(viewsets.ModelViewSet):
    serializer_class = AuthUserSimpleDataSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        if request.data['phone']:
            request.user.phone = request.data['phone']
        if request.user.check_password(request.data['old_password']):
            request.user.set_password(request.data['password'])
            request.user.save()
        response_data = self.get_serializer(request.user)
        return Response({"data": response_data.data, "isSuccess": True, "message": "Successfully password changed", "status": 200}, status=200)


class UserForgotPasswordEmailSendView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        email = request.data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            if user.first().is_email:
                token = default_token_generator.make_token(user.first())
                url = f"https://casamelhor.onrender.com/api/v1/account/user/forgot-password/verify/?token={token}&email={user.first().email}"
                _send_account_confirmation_email(user.first(), url=url)
                return Response({"data": None, "message": "Successfully email send", "isSuccess": True, "status": 200}, status=200)
            return Response({"data": None, "message": "Email is not verified", "isSuccess": True, "status": 200}, status=200)
        return Response({"data": None, "message": "User not found", "isSuccess": False, "status": 400}, status=200)


class UserForgotPasswordView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
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


class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Client admin Company Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(CompanyView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Client admin Company Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(CompanyView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Client admin Company Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(CompanyView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Client admin Company Delete Successfully", "isSuccess": True, "status": 200})


class RoleView(viewsets.ModelViewSet):
    serializer_class = AuthUserGroupOFPermissionsSerializer
    queryset = Role.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Client admin Company Get Successfully", "isSuccess": True, "status": 200})

    def create(self, request, *args, **kwargs):
        response_data = super(RoleView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Client admin Company Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        response_data = super(RoleView, self).update(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Client admin Company Edit Successfully", "isSuccess": True, "status": 200})

    def destroy(self, request, *args, **kwargs):
        super(RoleView, self).destroy(request, *args, **kwargs)
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Client admin Company Delete Successfully", "isSuccess": True, "status": 200})


class VaultView(viewsets.ModelViewSet):
    serializer_class = VaultSerializer
    queryset = Vault.objects.all()
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            serializer = self.get_serializer(self.get_object())
            return Response({"data": serializer.data, "message": "Client admin Company Get Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def create(self, request, *args, **kwargs):
        response_data = super(VaultView, self).create(request, *args, **kwargs)
        return Response({"data": response_data.data, "message": "Client admin Company Create Successfully", "isSuccess": True, "status": 200})

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            response_data = super(VaultView, self).update(request, *args, **kwargs)
            return Response({"data": response_data.data, "message": "Client admin Company Edit Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            super(VaultView, self).destroy(request, *args, **kwargs)
            serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
            return Response({"data": serializer.data, "message": "Client admin Company Delete Successfully", "isSuccess": True, "status": 200})
        return Response({"data": None, "message": "Unauthorized User", "isSuccess": False, "status": 401}, status=200)


class CasamelhorAdminView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Casamelhor Admin')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class CasamelhorBookingManagerView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Casamelhor Booking Manager')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class AuthUserPermissionsView(viewsets.ModelViewSet):
    serializer_class = AuthUserPermissionsSerializer
    queryset = Permission.objects.all()
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "Get All Auth User Permissions Successfully", "isSuccess": True, "status": 200})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"data": serializer.data, "message": "Auth User Permissions Get Successfully", "isSuccess": True, "status": 200})


class CasamelhorPropertyManagerView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Casamelhor Property Manager')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class ClientAdminView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Client Admin')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class ClientBookingManagerView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Client Booking Manager')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class ClientPropertyManagerView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Client Property Manager')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})


class GuestView(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    queryset = User.objects.filter(role__role='Guest')
    permission_classes = [IsSuperUser, ]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response({"data": serializer.data, "message": "All Client admin Companies Get Successfully", "isSuccess": True, "status": 200})
