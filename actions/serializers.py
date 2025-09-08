from rest_framework import serializers

from actions.models import Action


# ===== Секция Действий для выполнения привычек ===============================================
class ActionSerializer(serializers.ModelSerializer):
    habits_count = serializers.SerializerMethodField(read_only=True)

    def get_habits_count(self, obj):
        return obj.habits.count()


    class Meta:
        model = Action
        fields = [
            "id",
            "title",
            "habits_count",
        ]

class ActionTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['title']