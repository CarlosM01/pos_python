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
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemReadSerializer(many=True, read_only=True)
    items_data = SaleItemCreateSerializer(many=True, write_only=True, source='items')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'items', 'items_data', 'total_price']
    
    def validate_items_data(self, items):
        for item in items:
            product = item['product']
            quantity = item['quantity']
            try:
                product.check_stock(quantity)
            except ValueError as e:
                raise serializers.ValidationError(str(e))
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            product.reduce_stock(quantity)
            SaleItem.objects.create(
                sale=sale,
                **item_data
            )
        
        return sale
    