from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from habits.models import Habit
from habits.paginations import HabitPagination
from habits.serializers import HabitSerializer, HabitPublicSerializer, HabitCreateSerializer, HabitDetailsSerializer
from users.permissions import IsOwner
from habits.tasks import send_reminder

# ===== Секция привычек ===============================================
class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания новой привычки"""
    serializer_class = HabitCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitListAPIView(generics.ListAPIView):
    """Контроллер для получения списка привычек их владельца"""
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Контроллер для получения общедоступных привычек"""
    serializer_class = HabitPublicSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения детализации привычки"""
    queryset = Habit.objects.all()
    serializer_class = HabitDetailsSerializer
    permission_classes = (IsOwner | IsAdminUser,)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления привычки владельца"""
    queryset = Habit.objects.all()
    serializer_class = HabitCreateSerializer
    permission_classes = (IsOwner | IsAdminUser,)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления привычки владельца"""
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
