# tasks.py
from datetime import datetime
from celery import shared_task
from ..todo.models import Reminder
from ..todo.views import send_reminder

@shared_task
def send_reminders():
    reminders = Reminder.objects.filter(sent=False, reminder_time__lte=datetime.now())
    for reminder in reminders:
        send_reminder(reminder.todo)
        reminder.sent = True
        reminder.save()