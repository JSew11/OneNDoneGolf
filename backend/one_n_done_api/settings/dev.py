from .base import *

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS += [
    'reset_migrations',
]

RABBITMQ = {
    "PROTOCOL": "amqp",
    "HOST": os.getenv("RABBITMQ_HOST", "localhost"),
    "PORT": os.getenv("RABBITMQ_PORT", 5672),
    "USER": os.getenv("RABBITMQ_USER", "guest"),
    "PASSWORD": os.getenv("RABBITMQ_PASSWORD", "guest"),
    "VHOST": os.getenv("RABBITMQ_VHOST", "/")
}

CELERY_BROKER_URL = f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:{RABBITMQ['PASSWORD']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}/{RABBITMQ['VHOST']}"