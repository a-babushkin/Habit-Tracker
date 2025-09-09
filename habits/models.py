from django.db import models

from actions.models import Action
from places.models import Place
from users.models import User


class Habit(models.Model):
    """Модель полезных привычек"""

    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.CASCADE, related_name="habits", help_text="Выберите Владельца."
    )
    place = models.ForeignKey(
        Place, verbose_name="Место", on_delete=models.CASCADE, related_name="habits", help_text="Выберите место."
    )
    action = models.ForeignKey(
        Action,
        verbose_name="Действие",
        on_delete=models.CASCADE,
        related_name="habits",
        help_text="Выберите действие.",
    )
    time = models.TimeField(verbose_name="Время", help_text="Введите время выполнения привычки.")
    is_pleasant = models.BooleanField(
        verbose_name="Признак приятности", help_text="Укажите, приятна привычка или нет.", default=False
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Выберите связанную привычку",
        blank=True,
        null=True,
    )
    periodicity = models.IntegerField(
        verbose_name="Периодичность",
        default=1,
        help_text="Выберите периодичность.",
    )
    reward = models.CharField(
        max_length=255,
        verbose_name="Вознаграждение",
        help_text="Введите вознаграждение за выполнение привычки.",
        blank=True,
        null=True,
    )
    duration = models.IntegerField(
        verbose_name="Время на выполнение",
        help_text="Укажите время, необходимое для выполнения привычки (в секундах).",
    )
    is_public = models.BooleanField(verbose_name="Признак публичности", help_text="Укажите хотите поделиться или нет.")

    def __str__(self):
        return f"{self.action} {self.place} {self.time} {self.duration}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["action"]
