from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return False


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj or
            request.user.is_staff
        )
