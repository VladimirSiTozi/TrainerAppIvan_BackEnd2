from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TrainerAppIvan_BackEnd2.account'

    def ready(self):
        import TrainerAppIvan_BackEnd2.account.signals
