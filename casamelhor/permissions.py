from rest_framework.permissions import IsAdminUser, BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser or request.user.is_staff)
