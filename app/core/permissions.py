from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_staff
        return False


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
