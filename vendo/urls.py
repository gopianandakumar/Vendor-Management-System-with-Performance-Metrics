from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, PurchaseOrderViewSet, UserViewset

# Create a router and register the VendorViewSet with it
router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)
router.register(r'user', UserViewset)


urlpatterns = router.urls
