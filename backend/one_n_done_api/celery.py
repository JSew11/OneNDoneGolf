import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'one_n_done_api.settings')

app = Celery(
    'one_n_done_api',
    broker=os.environ.get('CELERY_BROKER')
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()