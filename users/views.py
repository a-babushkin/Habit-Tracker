from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from users.permissions import IsOwner
from users.serializer import UserSerializer


class UserCreateApiView(CreateAPIView):
    """Контроллер для создания (регистрации) нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """метод устанавливающий новой привычке владельца"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UsersListApiView(ListAPIView):
    """Контроллер получения списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ("id", "email")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["email"]


class UserRetrieveApiView(RetrieveAPIView):
    """Контроллер получения детализации пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsOwner,)


class UserUpdateApiView(UpdateAPIView):
    """Контроллер обновления пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsOwner,)


class UserDestroyApiView(DestroyAPIView):
    """Контроллер удаления пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser | IsOwner,)
