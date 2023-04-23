from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == "admin"
            or request.user.is_superuser
        )


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if (
            not request.user.is_authenticated
            and request.method in permissions.SAFE_METHODS
        ):
            return True
        elif request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.method == "POST"
        ):
            return True
        elif (
            request.user == obj.author
            or request.user.role == "moderator"
            or request.user.is_superuser
            or request.user.role == "admin"
        ) and request.method in ("DELETE", "PATCH", "PUT"):
            return True
