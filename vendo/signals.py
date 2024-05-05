# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from vendo.models import PurchaseOrderModel

@receiver(post_save, sender=PurchaseOrderModel)
def update_metrics_on_purchase_order_save(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivery_date:
        vendor = instance.vendor
        if vendor:
            vendor.update_metrics()

@receiver(post_delete, sender=PurchaseOrderModel)
def update_metrics_on_purchase_order_delete(sender, instance, **kwargs):
    vendor = instance.vendor
    if vendor:
        vendor.update_metrics()
