from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import VendorModel, PurchaseOrderModel
from django.contrib.auth.models import User



class VendorViewSetTestCase(APITestCase):
    def setUp(self):
        self.vendor_data = {
            "name": "Example Vendor",
            "contact_details": "example@example.com",
            "address": "123 Example St, Example City",
            "vendor_code": "VENDOR002",
            "on_time_delivery_rate": 0.95,
            "quality_rating_avg": 4.5,
            "average_response_time": 3600,
            "fulfillment_rate": 0.85
        }
        self.vendor = VendorModel.objects.create(**self.vendor_data)

    def test_retrieve_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor_data['name'])

    def test_update_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        updated_data = {
            "name": "Updated Vendor",
            "contact_details": "updated@example.com",
            "address": "456 Updated St, Updated City",
            "vendor_code": "VENDOR003",
            "on_time_delivery_rate": 0.90,
            "quality_rating_avg": 4.0,
            "average_response_time": 3000,
            "fulfillment_rate": 0.80
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(VendorModel.objects.filter(pk=self.vendor.pk).exists())

    def test_vendor_performance(self):
        url = reverse('vendor-performance', kwargs={'pk': self.vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['on_time_delivery_rate'], self.vendor_data['on_time_delivery_rate'])
        self.assertEqual(response.data['quality_rating_avg'], self.vendor_data['quality_rating_avg'])
        self.assertEqual(response.data['average_response_time'], self.vendor_data['average_response_time'])
        self.assertEqual(response.data['fulfillment_rate'], self.vendor_data['fulfillment_rate'])



class UserViewsetTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        updated_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User"
        }
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())




class PurchaseOrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.vendor = VendorModel.objects.create(name='Test Vendor', vendor_code='VENDOR001')
        self.purchase_order_data = {
            "po_number": "PO123",
            "vendor": self.vendor.id,
            "order_date": "2024-05-25",
            "delivery_date": "2024-06-10T08:00:00",
            "items": [{"name": "Item 1", "quantity": 10}, {"name": "Item 2", "quantity": 5}],
            "quantity": 15,
            "status": "pending",
            "quality_rating": 4.5,
            "issue_date": "2024-05-25T10:00:00",
            "acknowledgment_date": None
        }
        self.purchase_order = PurchaseOrderModel.objects.create(**self.purchase_order_data)

    def test_create_purchase_order(self):
        url = reverse('purchaseorder-list')
        response = self.client.post(url, self.purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrderModel.objects.count(), 2)

    def test_update_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        updated_data = self.purchase_order_data.copy()
        updated_data['status'] = 'completed'
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, 'completed')

    def test_delete_purchase_order(self):
        url = reverse('purchaseorder-detail', kwargs={'pk': self.purchase_order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PurchaseOrderModel.objects.filter(pk=self.purchase_order.pk).exists())

    def test_acknowledge_purchase_order(self):
        url = reverse('purchaseorder-acknowledge', kwargs={'pk': self.purchase_order.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)

