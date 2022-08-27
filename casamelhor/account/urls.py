from django.urls import path
from .views import *

urlpatterns = [
    path('', schema_view),
    path('register/', RegistrationView.as_view({'post': 'create'}), name='user_create'),
    path('update/<int:pk>/', RegistrationView.as_view({'put': 'update'}), name='user_update'),
    path('admin/user/get/', RegistrationView.as_view({'get': 'list'}), name='user_get'),
    path('admin/user/get/<int:pk>/', RegistrationView.as_view({'get': 'retrieve'}), name='user_get_one'),
    
    path('login/', LoginView.as_view({'post': 'create'}), name='user_update'),
    path('user/email/verify/', EmailVerificationView.as_view({'post': 'create'}), name='user_update'),
    path('user/email/resend/', ResendEmailOtpView.as_view({'post': 'create'}), name='user_update'),
    
    path('user/vault/create/', VaultView.as_view({'post': 'create'})),
    path('user/vault/get/', VaultView.as_view({'get': 'list'})),
    path('user/vault/get/<int:pk>/', VaultView.as_view({'get': 'retrieve'})),
    path('user/vault/edit/<int:pk>/', VaultView.as_view({'put': 'update'})),
    path('user/vault/delete/<int:pk>/', VaultView.as_view({'delete': 'destroy'})),

    path('user/profile/password-change/', UserPasswordChangeView.as_view({'post': 'create'})),
    path('user/forgot-password/', UserForgotPasswordEmailSendView.as_view({'post': 'create'})),
    path('user/forgot-password/verify/', UserForgotPasswordView.as_view({'post': 'create'})),

    path('role/permission/group/get/', RoleView.as_view({'get': 'list'})),
    path('role/permission/group/create/', RoleView.as_view({'post': 'create'})),
    path('role/permission/group/edit/<int:pk>/', RoleView.as_view({'put': 'update'})),
    path('role/permission/group/get/<int:pk>/', RoleView.as_view({'get': 'retrieve'})),
    path('role/permission/group/delete/<int:pk>/', RoleView.as_view({'delete': 'destroy'})),

    path('role/permission/get/', AuthUserPermissionsView.as_view({'get': 'list'})),
    path('role/permission/get/<int:pk>/', AuthUserPermissionsView.as_view({'get': 'retrieve'})),

    path('client/company/create/', CompanyView.as_view({'post': 'create'}), name='company_create'),
    path('client/company/get/', CompanyView.as_view({'get': 'list'}), name='company_get'),
    path('client/company/get/<int:pk>/', CompanyView.as_view({'get': 'retrieve'}), name='company_get_one'),
    path('client/company/edit/<int:pk>/', CompanyView.as_view({'put': 'update'}), name='company_edit'),
    path('client/company/delete/<int:pk>/', CompanyView.as_view({'delete': 'destroy'}), name='company_delete'),

    path('casamelhor/admin/user/get/', CasamelhorAdminView.as_view({'get': 'list'}), name='casamelhor_admin_user_get'),
    path('casamelhor/booking/manager/user/get/', CasamelhorBookingManagerView.as_view({'get': 'list'}), name='casamelhor_booking_manager_user_get'),
    path('casamelhor/property/manager/user/get/', CasamelhorPropertyManagerView.as_view({'get': 'list'}), name='casamelhor_property_manager_user_get'),
    path('client/admin/user/get/', ClientAdminView.as_view({'get': 'list'}), name='casamelhor_admin_user_get'),
    path('client/booking/manager/user/get/', ClientBookingManagerView.as_view({'get': 'list'}), name='client_booking_manager_user_get'),
    path('client/property/manager/user/get/', ClientPropertyManagerView.as_view({'get': 'list'}), name='casamelhor_property_manager_user_get'),
    path('guest/user/get/', GuestView.as_view({'get': 'list'}), name='guest_user_get'),
]
