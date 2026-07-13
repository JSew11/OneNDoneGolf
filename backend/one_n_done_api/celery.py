import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'one_n_done_api.settings')

RABBITMQ = {
    "PROTOCOL": "amqp", # change to "amqps" on prod
    "HOST": os.getenv("RABBITMQ_HOST", "localhost"),
    "PORT": os.getenv("RABBITMQ_PORT", 5672),
    "USER": os.getenv("RABBITMQ_USER", "guest"),
    "PASSWORD": os.getenv("RABBITMQ_PASSWORD", "guest"),
}

app = Celery(
    'one_n_done_api',
    broker=f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()