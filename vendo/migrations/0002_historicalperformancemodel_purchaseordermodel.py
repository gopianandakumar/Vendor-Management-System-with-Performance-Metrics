# Generated by Django 5.0.1 on 2024-05-02 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPerformanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('on_time_delivery_rate', models.FloatField()),
                ('quality_rating_avg', models.FloatField()),
                ('average_response_time', models.FloatField()),
                ('fulfillment_rate', models.FloatField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendo.vendormodel')),
            ],
            options={
                'verbose_name': 'HistoricalPerformanceModel',
                'verbose_name_plural': 'HistoricalPerformanceModels',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('order_date', models.DateField(auto_now_add=True, null=True)),
                ('delivery_date', models.DateTimeField(blank=True, null=True)),
                ('items', models.JSONField(null=True)),
                ('quantity', models.IntegerField(default=0, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=25)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('issue_date', models.DateTimeField()),
                ('acknowledgment_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendo.vendormodel')),
            ],
            options={
                'verbose_name': 'PurchaseOrderModel',
                'verbose_name_plural': 'PurchaseOrderModels',
            },
        ),
    ]