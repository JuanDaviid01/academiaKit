from rest_framework import viewsets, permissions, decorators, response, status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class IsAdminOrSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ("list", "create", "destroy"):
            return bool(request.user and request.user.is_staff)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and (request.user.is_staff or obj.pk == request.user.pk))

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    @decorators.action(detail=False, methods=["get", "patch"],
                       permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == "GET":
            ser = self.get_serializer(request.user)
            return response.Response(ser.data)
        ser = self.get_serializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response(self.get_serializer(request.user).data,
                                 status=status.HTTP_200_OK)
