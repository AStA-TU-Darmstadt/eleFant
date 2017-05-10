from django.apps import AppConfig


class ElefantConfig(AppConfig):
    name = 'elefant'

    # noinspection PyUnresolvedReferences
    def ready(self):
        # enable notifications here
        from .signals import successful_application_creation
