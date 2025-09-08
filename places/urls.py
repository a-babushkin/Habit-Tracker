from django.urls import path, include
from rest_framework.routers import SimpleRouter

from places.apps import PlacesConfig
from places.views import PlaceViewSet

app_name = PlacesConfig.name

router = SimpleRouter()
router.register(r"", PlaceViewSet)

urlpatterns = [
    path('', include(router.urls))
]
