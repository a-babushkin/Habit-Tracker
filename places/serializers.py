from rest_framework import serializers

from places.models import Place


# ===== Секция Мест выполнения привычек ===============================================
class PlaceSerializer(serializers.ModelSerializer):
    habits_count = serializers.SerializerMethodField(read_only=True)

    def get_habits_count(self, obj):
        return obj.habits.count()

    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "habits_count",
        ]


class PlaceTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['title']