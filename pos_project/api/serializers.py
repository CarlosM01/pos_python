from rest_framework import serializers
from .models import Product, Sale, SaleItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SaleItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']

class SaleItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemCreateSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'items']
    
    def to_representation(self, instance):
        self.fields['items'] = SaleItemReadSerializer(many=True)
        return super().to_representation(instance)
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            SaleItem.objects.create(
                sale=sale,
                **item_data
            )
        
        return sale
    