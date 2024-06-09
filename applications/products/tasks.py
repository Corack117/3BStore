from celery import shared_task

from .models import Product
from applications.orders.utils import notificate_low_stock

@shared_task
def check_inventory_stock():
    products = Product.objects.filter(stock__lt=10)
    notificate_low_stock(products)