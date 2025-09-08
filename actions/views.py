from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from actions.models import Action
from actions.serializers import ActionSerializer


# ===== Секция Действий для выполнения привычек ===============================================
class ActionViewSet(ModelViewSet):
    """Контроллер для работы с Местами"""

    queryset = Action.objects.all().order_by("title")
    serializer_class = ActionSerializer
    permission_classes = (IsAdminUser,)
