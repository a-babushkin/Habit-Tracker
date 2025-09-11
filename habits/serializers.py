from rest_framework import serializers

from actions.serializers import ActionTitleSerializer
from habits.models import Habit
from habits.validators import (MaxDurationValidator, NoRewardForPleasantHabitValidator, PeriodicityValidator,
                               PleasantHabitRelatedValidator, RewardOrRelatedHabitValidator)
from places.serializers import PlaceTitleSerializer


# ===== Секция привычек ===============================================
class HabitSerializer(serializers.ModelSerializer):
    action = ActionTitleSerializer(read_only=True)
    place = PlaceTitleSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = [
            "id",
            "owner",
            "action",
            "place",
            "time",
            "duration",
            "is_pleasant",
            "periodicity",
            "is_public",
        ]


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardOrRelatedHabitValidator(),
            PleasantHabitRelatedValidator(),
            NoRewardForPleasantHabitValidator(),
            MaxDurationValidator(),
            PeriodicityValidator(),
        ]


class HabitPublicSerializer(serializers.ModelSerializer):
    action = ActionTitleSerializer(read_only=True)
    place = PlaceTitleSerializer(read_only=True)

    class Meta:
        model = Habit
        fields = ("action", "is_pleasant", "time", "place")


class HabitDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
