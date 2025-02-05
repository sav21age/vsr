from django.apps import AppConfig


class RosesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roses'
    verbose_name = '13. Каталог роз'

    def ready(self):
        import common.signals
