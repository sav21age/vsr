from django.apps import AppConfig


class DeciduousConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deciduous'
    verbose_name = '02. Каталог лиственных растений'

    def ready(self):
        import common.signals
