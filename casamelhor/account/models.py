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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='role_group', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role


class Company(models.Model):
    company_name = models.CharField(max_length=255)
    address1 = models.TextField(max_length=20000, null=True, blank=True)
    address2 = models.TextField(max_length=20000, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    gst_number = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='user_role')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='user_company')
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


document_choices = (('Aadhar card', 'Aadhar card'), ('Driving Licence', 'Driving Licence'), ('Passport', 'Passport'))


class Vault(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users_vault")
    is_indian = models.BooleanField(default=True)
    type = models.CharField(max_length=255, choices=document_choices, null=True, blank=True)
    document = VersatileImageField(upload_to="profile/", ppoi_field='ppoi', null=True, blank=True)
    passport_photo = VersatileImageField(upload_to="profile/", ppoi_field='ppoi', null=True, blank=True)
    visa_photo = VersatileImageField(upload_to="profile/", ppoi_field='ppoi', null=True, blank=True)
    address1 = models.TextField(max_length=20000, null=True, blank=True)
    address2 = models.TextField(max_length=20000, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)
    passport_number = models.CharField(max_length=255, null=True, blank=True)
    passport_country_of_issued = models.CharField(max_length=255, null=True, blank=True)
    passport_date_of_issued = models.DateField(null=True, blank=True)
    passport_expire_date = models.DateField(null=True, blank=True)
    visa_issued_date = models.DateField(null=True, blank=True)
    visa_expire_date = models.DateField(null=True, blank=True)
    visa_type = models.CharField(max_length=255, null=True, blank=True)
    ppoi = PPOIField('Image PPOI')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.passport_number
