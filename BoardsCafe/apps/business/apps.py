from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BoardsCafe.apps.business'
    label = 'business'
    verbose_name = 'Business Settings'