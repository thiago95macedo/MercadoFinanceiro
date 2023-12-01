from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iqoption'

    def ready(self):
        import iqoption.signals  # Importa os sinais no método ready