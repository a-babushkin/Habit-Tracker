from django.contrib import admin
from habits.models import Habit, Place, Action


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "periodicity", "duration")
