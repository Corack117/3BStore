from django.db import transaction
from rest_framework import serializers
from common.serializers import BaseSerializer
from rest_framework.fields import DateTimeField
from rest_framework_mongoengine.serializers import DocumentSerializer

from .constants import ErrorCode
from .models import Order, OrderDetail
from .exceptions import FiledToCreateOrder
from .utils import cancel_order_by_inssuficiente_stock, convert_to_currency, get_products, get_total_of_purchase, notificate_low_stock, validate_inssuficient_stock, validate_stock
from applications.products.models import Product
from applications.products.serializers import SimpleProductSerializer
from .mongo_models import ProductMongo, PurchaseMongo

class CorrectCurrencySerializer(BaseSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = convert_to_currency(data['total'])
        return data

class OrderSerializer(CorrectCurrencySerializer):
    id = serializers.UUIDField(read_only=True, source='slug')

    class Meta:
        model = Order
        exclude = ['slug']

class PurchaseSerializer(CorrectCurrencySerializer):
    user_id = serializers.UUIDField(write_only=True, required=True)
    products = serializers.ListField(child=SimpleProductSerializer(), write_only=True, required=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'slug',
            'user',
            'num_products',
            'total',
            'active',
            'created',
            'updated'
        ]

    def create(self, validated_data):
        user_id = validated_data['user_id']
        products: list[Product] = get_products(validated_data['products'])
        num_products = sum([product['quantity'] for product in validated_data['products']])
        total = get_total_of_purchase(products, validated_data)

        order = None
        product_low_stock = []
        products_inssuficient_stock = []
        try: 
            with transaction.atomic():
                order = Order.objects.create(user_id=user_id, num_products=num_products, total=total)
                mongo_products = []
                for product in products:
                    product_finded = [data for data in validated_data['products'] if data['product_id'] == product.slug][0]
                    OrderDetail.objects.create(order=order, product=product, quantity=product_finded['quantity'], unit_price=product.price)
                    product.stock -= product_finded['quantity']

                    if validate_stock(product):
                        product_low_stock.append(product)
                    if validate_inssuficient_stock(product):
                        products_inssuficient_stock.append({'instance': product, 'current_stock': product_finded['quantity']}) 
                    else:
                        product.save()

                    mongo_products.append(
                        ProductMongo(
                            product_id=str(product.slug), 
                            name=product.name, 
                            unit_price=product.price, 
                            quantity=product_finded['quantity'], 
                            subtotal=product.price * product_finded['quantity']
                        )
                    )

                if len(products_inssuficient_stock) > 0:
                    cancel_order_by_inssuficiente_stock(products_inssuficient_stock)
                    
                mongo_purchase = PurchaseMongo(
                    purchase_id=str(order.slug), 
                    user_id=str(user_id), 
                    products=mongo_products, 
                    total=total
                )
                mongo_purchase.save()
                
        except serializers.ValidationError as e:
            raise e
        except:
            raise FiledToCreateOrder()

        notificate_low_stock(product_low_stock)
        return order

class TicketProductSerializer(DocumentSerializer):
    class Meta:
        model = ProductMongo
        fields = [
            'product_id',
            'name',
            'unit_price',
            'quantity',
            'subtotal'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['unit_price'] = convert_to_currency(data['unit_price'])
        data['subtotal'] = convert_to_currency(data['subtotal'])
        return data

class TicketSerializer(DocumentSerializer):
    date = DateTimeField(format='%Y-%m-%dT%H:%M:%S.%f', input_formats=['%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'])
    products = TicketProductSerializer(many=True)

    class Meta:
        model = PurchaseMongo
        depth = 4
        fields = [
            'purchase_id',
            'user_id',
            'products',
            'total',
            'date'
        ]