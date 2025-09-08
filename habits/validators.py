from django.core.exceptions import ValidationError


class RewardOrRelatedHabitValidator:
    """Валидатор исключающий одновременное задание reward и related_habit."""

    def __call__(self, attrs):
        if attrs.get('reward') and attrs.get('related_habit'):
            raise ValidationError("Нельзя одновременно задать поля 'Вознаграждение' и 'Связанная привычка'. "
                                  "Заполните только одно из них.")


class PleasantHabitRelatedValidator:
    """Валидатор для ограничения связанных привычек."""

    def __call__(self, attrs):
        related_habit = attrs.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "Привычка может быть связана только с теми, у которых установлена отметка 'Приятная привычка'")


class MaxDurationValidator:
    """Валидатор максимальной продолжительности выполнения привычки."""

    def __call__(self, attrs):
        duration = attrs.get('duration')
        if duration > 120:
            raise ValidationError("Максимальное время выполнения привычки — 120 секунд.")


class PeriodicityValidator:
    """Валидатор минимальной периодичности привычки."""

    def __call__(self, attrs):
        value = attrs.get('periodicity')
        if value < 1 or value > 7:
            raise ValidationError("Минимальная частота выполнения привычки — раз в 1 день, "
                                  "максимальная — раз в 7 дней.")


class NoRewardForPleasantHabitValidator:
    """Валидатор запрета награждения приятной привычки."""

    def __call__(self, attrs):
        if attrs.get('is_pleasant') and (attrs.get('reward') or attrs.get('related_habit')):
            raise ValidationError("Приятной привычке нельзя присваивать вознаграждение или связанную привычку.")


class NoBothRewardAndRelatedHabitValidator:
    """Валидатор запрета задавать значение одновременно вознаграждению и связанной привычке."""

    def __call__(self, attrs):
        if attrs.get('reward') and attrs.get('related_habit'):
            raise ValidationError("Привычке нельзя присваивать вознаграждение и связанную привычку одновременно.")
