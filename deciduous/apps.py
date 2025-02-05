from django.apps import AppConfig


class DeciduousConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deciduous'
    verbose_name = '07. Каталог лиственных растений'

    def ready(self):
        import common.signals
