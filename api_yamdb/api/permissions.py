from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdministratorRole(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser
                )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser
                )


class IsSuperuserAdminModeratorAuthorOrReadOnly(BasePermission):
    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_permission(self, request, view):
        safe_method = request.method in SAFE_METHODS
        return safe_method or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        safe_method = request.method in SAFE_METHODS
        return safe_method or (
            request.user == obj.author
            or request.user.is_authenticated and (
                request.user.is_admin or request.user.is_moderator
            ))
