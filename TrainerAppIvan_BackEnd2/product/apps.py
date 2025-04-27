from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TrainerAppIvan_BackEnd2.product'

    def ready(self):
        # Import signals here
        import TrainerAppIvan_BackEnd2.product.signals
