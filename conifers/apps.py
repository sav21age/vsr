from django.apps import AppConfig


class ConifersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conifers'
    verbose_name = '19. Каталог хвойных растений'

    def ready(self):
        import common.signals
