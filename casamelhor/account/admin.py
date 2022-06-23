from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *
from .forms import AdminForm


class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role"]

    def get_ordering(self, request):
        return ["-id"]


class UserAdmin(admin.ModelAdmin):
    form = AdminForm
    list_display = ["id", "email", "phone", 'is_active']
    search_fields = ["email", "phone"]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
