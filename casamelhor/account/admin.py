from django.contrib import admin
from .models import *


class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role"]

    def get_ordering(self, request):
        return ["-id"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "phone", 'is_active']
    search_fields = ["email", "phone"]

    def get_ordering(self, request):
        return ["-id"]


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Company)
admin.site.register(Vault)
admin.site.register(Permission)
