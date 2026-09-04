from django.apps import AppConfig


class QueueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'queue_app'
    label = 'queue'
