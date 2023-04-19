from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_authenticated:
            if user.is_admin or user.is_moderator:
                return True
            if obj.author == user:
                return True
        return False


class IsAuthorOrAdminOrModeratorComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_authenticated:
            if user.is_admin or user.is_moderator:
                return True
            if obj.author == user:
                return True
            if obj.review.author == user:
                return True
        return False