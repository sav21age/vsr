from django.apps import AppConfig


class OtherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'other'
    verbose_name = '22. Сопутствующие товары'

    def ready(self):
        import common.signals
