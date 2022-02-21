from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'management'


# class DepConfig(AppConfig):
#     name = 'management'

#     def ready(self):
#         import management.signals   