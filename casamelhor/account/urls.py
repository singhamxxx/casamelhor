from django.urls import path
from .views import *

urlpatterns = [
    path('', schema_view),
    path('register/', RegistrationView.as_view({'post': 'create'}), name='user_create'),
    path('update/', user_update_profile_view),
    path('update/<int:id>/', user_update_profile_view),
    path('login/', user_login_view),
    path('admin/user/get/', user_get_view),
    path('admin/user/get/<int:id>/', user_get_view),
    path('user/email/verify/', email_verification_view),
    path('user/email/resend/', resend_email_otp_view),
    path('user/vault/create/', create_user_vault_view),
    path('user/profile/password-change/', user_password_change_view),
    path('user/forgot-password/', user_forgot_password_email_send_view),
    path('user/forgot-password/verify/', user_forgot_password_view),
    path('role/permission/group/get/', user_group_of_permissions_view),
    path('role/permission/group/create/', create_user_group_of_permissions_view),
    path('role/permission/group/edit/<int:id>/', edit_user_group_of_permissions_view),
    path('role/permission/group/get/<int:id>/', user_group_of_permissions_view),
    path('role/permission/get/', user_permission_view),
    path('role/permission/get/<int:id>/', user_permission_view),

    path('client/company/create/', CompanyView.as_view({'post': 'create'}), name='company_create'),
    path('client/company/get/', CompanyView.as_view({'get': 'list'}), name='company_create'),
    path('client/company/get/<int:pk>/', CompanyView.as_view({'get': 'retrieve'}), name='company_create'),
    path('client/company/edit/<int:pk>/', CompanyView.as_view({'put': 'update'}), name='company_create'),
    path('client/company/delete/<int:pk>/', CompanyView.as_view({'delete': 'destroy'}), name='company_create'),

]
