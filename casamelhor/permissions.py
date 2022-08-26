from rest_framework.permissions import IsAdminUser, BasePermission, IsAuthenticated


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser or request.user.is_staff)


class IsCasamelhorBookingManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Casamelhor Booking Manager")


class IsCasamelhorPropertyManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Casamelhor Property Manager")


class IsClientAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Client Admin")


class IsClientBookingManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Client Booking Manager")


class IsClientPropertyManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Client Property Manager")


class IsGuestUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role.role == "Guest")


class IsBookingUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_superuser or request.user.is_staff or request.user.role.role == "Casamelhor Booking Manager" or request.user.role.role == "Client Booking Manager")
