import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'send_mail_every_week': {
        'task': 'portal.tasks.get_week_notification',
        'schedule': crontab(hour=8, minute=0, day_of_week='mon'),

    }
}

app.autodiscover_tasks()