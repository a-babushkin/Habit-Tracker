from django.urls import include, path
from rest_framework.routers import SimpleRouter

from actions.apps import ActionsConfig
from actions.views import ActionViewSet

app_name = ActionsConfig.name

router = SimpleRouter()
router.register(r"", ActionViewSet)

urlpatterns = [path("", include(router.urls))]
