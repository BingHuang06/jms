from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAdminUserOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and  request.user.is_authenticated and
            (request.method in SAFE_METHODS or request.user.is_superuser)
        )
