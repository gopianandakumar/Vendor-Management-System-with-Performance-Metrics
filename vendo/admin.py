from django.contrib import admin

from vendo.models import HistoricalPerformanceModel, PurchaseOrderModel, VendorModel

# Register your models here.
@admin.register(VendorModel)
class VendorModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor_code']


@admin.register(PurchaseOrderModel)
class VendorModelAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'status']

@admin.register(HistoricalPerformanceModel)
class VendorModelAdmin(admin.ModelAdmin):
    list_display = ['on_time_delivery_rate', 'fulfillment_rate']


    