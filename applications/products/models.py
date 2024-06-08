from uuid import uuid4
from django.db import models

# Create your models here.

class Product(models.Model):
    slug = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name='slug', db_index=True)

    sku = models.CharField(unique=True, max_length=50, null=False, blank= False)
    name = models.CharField(max_length=50, null=False, blank= False)
    description = models.CharField(max_length=200, null=True, blank= True)
    price = models.PositiveIntegerField(null=False, blank=False)
    stock = models.PositiveIntegerField(default=100, null=False, blank=False)
    active = models.BooleanField(default=True, null=True, blank=False)
    created = models.DateTimeField(verbose_name="Creado", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Actualizado", auto_now=True)