from datetime import datetime
from rest_framework.serializers import ValidationError

from .models import Order, OrderDetail, ProductReturn
from .exceptions import DuplicatedProductIDs
from applications.products.models import Product
from config.settings.base import logger

def get_products(products: list):
    product_ids = [product['product_id'] for product in products]
    if len(product_ids) != len(set(product_ids)):
        raise DuplicatedProductIDs()
    return Product.objects.filter(slug__in=product_ids)

def get_total_of_purchase(products: list[Product], validated_data: dict):
    total = 0
    for product in products:
        product_finded = [data for data in validated_data['products'] if data['product_id'] == product.slug][0]
        total += product.price * product_finded['quantity']
    return total


def convert_to_currency(value: int):
    return '${:,.2f}'.format(value / 100)

def notificate_low_stock(product_low_stock: list[Product]):
    if len(product_low_stock) == 0:
        return

    logger.info('----------------------------------------')
    for product in product_low_stock:
        logger.info(f'Product with low stock:')
        logger.info(f'ID: {product.slug}')
        logger.info(f'NAME: {product.name}')
        logger.info(f'CURRENT SOTCK: {product.stock}')
        logger.info('----------------------------------------')

def validate_stock(product: Product):
    if product.stock < 10:
        return True
    
def validate_inssuficient_stock(product: Product):
    if product.stock < 0:
        return True 
    
def cancel_order_by_inssuficiente_stock(products: list[dict[str: Product | int]]):
    if len(products) == 0:
        return
    
    messages = []
    for product in products:
        message = {
            'error': 'Product with insufficient stock',
            'id': product['instance'].slug,
            'name': product['instance'].name,
            'current_stock': product['current_stock']
        }
        messages.append(message)

    notificate_low_stock([product['instance'] for product in products])
    raise ValidationError(messages)

def convert_bson_dates(data):
    for key, value in data.items():
        if isinstance(value, dict) and '$date' in value:
            data[key] = datetime.fromtimestamp(value['$date'] / 1000.0).isoformat()
        elif isinstance(value, list):
            for item in value:
                convert_bson_dates(item)
        elif isinstance(value, dict):
            convert_bson_dates(value)
    return data