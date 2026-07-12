from django.apps import AppConfig


class TarrifsConfig(AppConfig):
    name = 'tariffs'

    def ready(self):
        import tariffs.signals
