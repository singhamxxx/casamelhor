from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from versatileimagefield.fields import VersatileImageField, PPOIField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Mobile must be set'))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    role = models.CharField(max_length=100, unique=True)
    permission = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='role_permission')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='user_role')
    login_ip = models.CharField(max_length=255, null=True, blank=True)
    employee_id = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    email_otp = models.IntegerField(null=True, blank=True)
    phone_otp = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    image = VersatileImageField(upload_to="profile/", blank=True, null=True, ppoi_field='ppoi')
    ppoi = PPOIField()
    is_email = models.BooleanField(default=False)
    is_phone = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'


class Vault(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_vault")
    is_indian = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class IndianVault(models.Model):
    document_choices = (('Aadhar card', 'Aadhar card'), ('Driving Licence', 'Driving Licence'), ('Passport', 'Passport'))
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE, related_name="indian_users_vault")
    type = models.CharField(max_length=255, choices=document_choices)
    document = VersatileImageField(upload_to="profile/", ppoi_field='ppoi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type


class ForeignersVault(models.Model):
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE, related_name="foreigners_users_vault")
    passport_photo = VersatileImageField(upload_to="profile/", ppoi_field='ppoi')
    visa_photo = VersatileImageField(upload_to="profile/", ppoi_field='ppoi')
    address1 = models.TimeField(max_length=20000)
    address2 = models.TimeField(max_length=20000)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=255)
    passport_country_of_issued = models.CharField(max_length=255)
    passport_date_of_issued = models.DateField()
    passport_expire_date = models.DateField()
    visa_issued_date = models.DateField()
    visa_expire_date = models.DateField()
    visa_type = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.passport_number
