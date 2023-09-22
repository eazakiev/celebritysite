from django.apps import AppConfig


class WomenConfig(AppConfig):
    """Класс конфигурации приложения Women.
    Args:
        AppConfig (class): _description_
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    verbose_name = 'Женщины мира'
