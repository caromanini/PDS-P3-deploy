from django.apps import AppConfig


class LockersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lockers'

    def ready(self):
        from . import mqtt_client, signals
