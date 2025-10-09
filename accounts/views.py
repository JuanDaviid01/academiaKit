from rest_framework import viewsets, permissions, decorators, response, status # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from core.permissions import IsAdminOrSelf
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSelf]

    # Búsqueda útil opcional
    search_fields = ("username", "email", "first_name", "last_name", "document_id")
    ordering_fields = ("id", "username", "email", "date_joined", "last_login")

    @decorators.action(detail=False, methods=["get", "patch"], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == "GET":
            return response.Response(self.get_serializer(request.user).data)
        ser = self.get_serializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return response.Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)