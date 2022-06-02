from django.db import models
from django.contrib.auth.models import AbstractUser, Group
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
    key = models.TextField(max_length=20000, null=True, blank=True)
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


