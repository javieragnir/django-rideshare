from django.contrib.auth import get_user_model
from rest_framework import viewsets

from config.permissions import AdminOnlyPermission

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOnlyPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
