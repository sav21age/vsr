from django.apps import AppConfig


class FruitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fruits'
    verbose_name = '10. Каталог плодовых растений'

    def ready(self):
        import common.signals
