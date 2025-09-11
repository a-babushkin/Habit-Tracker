from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView, HabitPublicListAPIView,
                          HabitRetrieveAPIView, HabitUpdateAPIView)

app_name = HabitsConfig.name

router = SimpleRouter()
urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="habit-create"),
    path("public/", HabitPublicListAPIView.as_view(), name="public-list"),
    path("list/", HabitListAPIView.as_view(), name="habit-list"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit-detail"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit-update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit-delete"),
]
urlpatterns += router.urls
