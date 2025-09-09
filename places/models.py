from django.db import models


class Place(models.Model):
    """Модель места, в котором необходимо выполнять привычку."""

    title = models.CharField(
        max_length=255,
        verbose_name="Наименование",
        help_text="Введите наименование места, где вы будете выполнять свою привычку.",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        ordering = ["title"]
