from django.apps import AppConfig


class AntraegeConfig(AppConfig):
    name = 'antraege'

    # noinspection PyUnresolvedReferences
    def ready(self):
        # enable notifications here
        from .signals import successful_application_creation
