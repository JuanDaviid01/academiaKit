# core/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS # type: ignore

# comprueba si es admin
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

# los admin pueden ver y crear
# Los usuarios normales pueden ver
# los incognitos no pueden ni ver ni editar
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)

# El admin puede editar todo
# El usuario puede modificar su propia informacion
class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        if getattr(view, "action", None) in ("list", "create", "destroy"):
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user.is_staff or obj.pk == request.user.pk))
