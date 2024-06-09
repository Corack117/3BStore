from rest_framework import serializers
from common.serializers import BaseSerializer

from .models import Product

class ProductSerializer(BaseSerializer):
    active = serializers.BooleanField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Product
        exclude = ['slug']

class AddStockSerializer(BaseSerializer):
    add_to_stock = serializers.IntegerField(min_value=1, write_only=True, required=True)
    sku = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        exclude = ['slug']
    
    def update(self, instance, validated_data):
        instance.stock += validated_data.get('add_to_stock', 0)
        instance.save()
        return instance
    
class SimpleProductSerializer(BaseSerializer):
    product_id = serializers.UUIDField(write_only=True, required=True)
    quantity = serializers.IntegerField(min_value=1, write_only=True, required=True)

    class Meta:
        model = Product
        fields = [
            'product_id',
            'quantity'
        ]