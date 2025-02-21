from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Sale, SaleItem
from .serializers import (
    ProductSerializer, 
    SaleSerializer, 
    SaleItemCreateSerializer, 
    SaleItemReadSerializer
)
from django.db import models

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    
    def get_queryset(self):
        return Sale.objects.annotate(
            total_price=models.Sum(
                models.F('items__product__price') * models.F('items__quantity')
            )
        )
    serializer_class = SaleSerializer

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    
    def get_queryset(self):
        return SaleItem.objects.annotate(
            subtotal=models.F('product__price') * models.F('quantity')
        )
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SaleItemCreateSerializer
        return SaleItemReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
