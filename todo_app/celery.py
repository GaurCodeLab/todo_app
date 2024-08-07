
from celery import Celery
from celery.schedules import crontab
from . import *


app= Celery('todo_app', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'send-reminders': {
        'task': 'tasks.send_reminders',
        'schedule': crontab(minute='*'),
    },
}