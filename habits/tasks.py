from datetime import datetime

import requests
from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_reminder() -> None:
    """Отправка напоминаний на телеграм пользователям."""

    habits = Habit.objects.all()
    current_time = datetime.now()

    for habit in habits:
        habit_time_full = datetime.combine(current_time.date(), habit.time)

        if current_time > habit_time_full:
            text = f"Вам нужно сделать {habit.action} в {habit.place} в {habit.time}"
            params = {
                "text": text,
                "chat_id": habit.owner.tg_chat_id,
            }
            requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
