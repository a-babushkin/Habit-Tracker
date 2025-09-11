from django.db import models


class Action(models.Model):
    """Модель действия для закрепления привычки"""

    title = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите наименование действия, которое необходимо выполнить.",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ["title"]
