from django.apps import AppConfig


class PerennialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'perennials'
    verbose_name = '03. Каталог многолетних растений'

    def ready(self):
        import common.signals
