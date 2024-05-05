from datetime import datetime, timezone
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from vendo.models import PurchaseOrderModel, VendorModel
from vendo.serializers import UserSerializer, VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = VendorModel.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_metrics = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfilment_rate": vendor.fulfillment_rate
        }
        return Response(performance_metrics)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        
        if purchase_order.status != PurchaseOrderModel.PENDING:
            return Response({"message": "Cannot acknowledge a purchase order that is not pending."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update acknowledgment_date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Recalculate average_response_time
        purchase_orders = PurchaseOrderModel.objects.filter(vendor=purchase_order.vendor, acknowledgment_date__isnull=False)
        total_response_time = sum((po.acknowledgment_date - po.issue_date).total_seconds() for po in purchase_orders)
        average_response_time = total_response_time / purchase_orders.count() if purchase_orders.count() > 0 else None
        purchase_order.vendor.average_response_time = average_response_time
        purchase_order.vendor.save()

        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)
    
from django.contrib.auth.models import User

class UserViewset(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = User.objects.all()

    serializer_class = UserSerializer

    def create(self, request):
        request_data = request.data.copy()
        request_data['date_joined'] = datetime.now(timezone.utc)
        request_data['is_staff'] = False
        request_data['is_active'] = True
        serialzier = self.get_serializer(data=request_data)
        if serialzier.is_valid():
            user = serialzier.save()
            user.set_password('password')
            user.save()
            return Response({'detail':'Created User Successfully'}, 201)
        else:
            return Response(serialzier.errors, 400)

    @action(detail=False, methods=['post'])
    def login(self, request):
        user = self.get_queryset().get(email=request.data['email'])
        token = Token()
        token.user = user
        token.save()
        return Response({'AuthToken': token.key})

    def logout(self, request):
        pass
