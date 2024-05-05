from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class VendoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vendo'

    def ready(self) -> None:
        from .models import PurchaseOrderModel
        from .signals import update_metrics_on_purchase_order_delete, update_metrics_on_purchase_order_save

        post_save.connect(update_metrics_on_purchase_order_save, sender=PurchaseOrderModel)
        return super().ready()
