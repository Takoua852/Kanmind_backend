from rest_framework.permissions import BasePermission


class AllowAny(BasePermission):

    """
    Permission class that grants access to any user, authenticated or not.

    Usage:
    - Can be used on views that should be publicly accessible (e.g., login, registration, public APIs).

    Example:
        permission_classes = [AllowAny]
    """
    def has_permission(self, request, view):
        return True