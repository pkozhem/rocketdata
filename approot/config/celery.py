import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'increase-debt-beat': {
        'task': 'src.entities.tasks.increase_debt_beat',
        'schedule': crontab(hour='*/3', minute=0)
    },
    'decrease-debt-beat': {
        'task': 'src.entities.tasks.decrease_debt_beat',
        'schedule': crontab(hour=6, minute=30)
    }
}
