import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsChannel.settings')

app = Celery('NewsChannel')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'when_creating_post': {
        'task': 'news.tasks.notify_about_new_post',
        'schedule': 30,
        'args': ("some_arg"),
    },
}
app.conf.beat_schedule = {
    'when_week': {
        'task': 'news.tasks.notify_weekly',
        'schedule': 30,
        #'schedule': crontab(day_of_week="fri", hour="18", minute="00"),
    },
}


