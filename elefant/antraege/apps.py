from django.apps import AppConfig


class AntraegeConfig(AppConfig):
    name = 'antraege'

    def ready(self):
        # enable notifications here
        from .signals import send_email_upon_application_creation
