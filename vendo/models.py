from django.db import models
from django.db.models import Count, Avg, F

# Create your models here.

class VendorModel(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_details = models.TextField(null=True)
    address = models.TextField(null=True)
    vendor_code = models.CharField(max_length=100, null=True, blank=True, unique=True)
    on_time_delivery_rate = models.FloatField(null = True)
    quality_rating_avg = models.FloatField(null = True)
    average_response_time = models.FloatField(null = True)
    fulfillment_rate = models.FloatField(null = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "VendorModel"
        verbose_name_plural = "VendorModels"



    def update_metrics(self):
        self.on_time_delivery_rate = self.calculate_on_time_delivery_rate()

        self.quality_rating_avg = self.calculate_quality_rating_average()

        self.average_response_time = self.calculate_average_response_time()

        self.fulfillment_rate = self.calculate_fulfillment_rate()

        self.save()
    
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseordermodel_set.filter(status='completed')

        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('acknowledgment_date'))

        on_time_delivery_rate = (on_time_delivered_pos.count() / completed_pos.count()) if completed_pos.count() > 0 else 0

        return on_time_delivery_rate

    def calculate_quality_rating_average(self):
        completed_pos_with_rating = self.purchaseordermodel_set.filter(status='completed', quality_rating__isnull=False)

        quality_rating_average = completed_pos_with_rating.aggregate(Avg('quality_rating'))['quality_rating__avg']

        if quality_rating_average is not None:
            return quality_rating_average
        else:
            return 0
    
    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseordermodel_set.filter(acknowledgment_date__isnull=False)

        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in acknowledged_pos]

        if response_times:
            average_response_time = sum(response_times) / len(response_times)
            return average_response_time
        else:
            return 0

    def calculate_fulfillment_rate(self):
        successful_pos = self.purchaseordermodel_set.filter(status='completed').count()

        total_pos = self.purchaseordermodel_set.count()

        if total_pos > 0:
            fulfillment_rate = successful_pos / total_pos
            return fulfillment_rate
        else:
            return 0

    

class PurchaseOrderModel(models.Model):

    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    vendor =  models.ForeignKey(VendorModel, on_delete=models.CASCADE, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(null=True)
    quantity = models.IntegerField(default=0, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=PENDING)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        pass
    
    class Meta:
        verbose_name = "PurchaseOrderModel"
        verbose_name_plural = "PurchaseOrderModels"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.calculate_on_time_delivery_rate()
        self.vendor.calculate_quality_rating_average()
        self.vendor.calculate_average_response_time()
        self.vendor.calculate_fulfillment_rate()

class HistoricalPerformanceModel(models.Model):
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        verbose_name = "HistoricalPerformanceModel"
        verbose_name_plural = "HistoricalPerformanceModels"

   