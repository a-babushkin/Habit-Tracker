from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from places.models import Place
from places.serializers import PlaceSerializer


# ===== Секция Мест выполнения привычек ===============================================
class PlaceViewSet(ModelViewSet):
    """Контроллер для работы с Местами"""

    queryset = Place.objects.all().order_by("title")
    serializer_class = PlaceSerializer
    permission_classes = (IsAdminUser,)
