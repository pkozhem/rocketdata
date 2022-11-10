from rest_framework.permissions import BasePermission


class IsActivePermission(BasePermission):
    """ 5. Restrict permission for users which is_active status is False. """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_active,
        )
