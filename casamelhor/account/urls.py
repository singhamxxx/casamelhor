from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', registration_view),
    path('login/', user_login_view),
    path('user/email/verify/', email_verification_view),
    path('user/email/resend/', resend_email_view),
    path('user/profile/password-change/', user_password_change_view),
    path('user/forgot-password/', user_forgot_password_email_send_view),
    path('user/forgot-password/verify/', user_forgot_password_view),
]