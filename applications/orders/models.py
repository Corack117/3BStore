from uuid import uuid4
from django.db import models
from mongoengine import Document, StringField, IntField

from applications.users.models import User
from applications.products.models import Product

# Create your models here.

class Order(models.Model):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='Slug', db_index=True)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    num_products = models.PositiveIntegerField(null=False, blank=False)
    total = models.PositiveIntegerField(null=False, blank=False)
    active = models.BooleanField(default=True, null=True, blank=False)
    created = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Updated", auto_now=True)

class OrderDetail(models.Model):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='Slug', db_index=True)

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    unit_price = models.PositiveIntegerField(null=False, blank=False)
    active = models.BooleanField(default=True, null=True, blank=False)
    created = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Updated", auto_now=True)

class ProductReturn(models.Model):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='Slug', db_index=True)
    
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=False, blank=False)
    quantity = models.PositiveIntegerField(null=False, blank=False)
    refunded_amount = models.PositiveIntegerField(null=False, blank=False)
    active = models.BooleanField(default=True, null=True, blank=False)
    created = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Updated", auto_now=True)