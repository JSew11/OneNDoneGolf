import os

from celery import Celery

# todo - change this to use 'one_n_done_api.settings.base' when deploying
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'one_n_done_api.settings.dev')

app = Celery('one_n_done_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['golf_pickem.tasks'])