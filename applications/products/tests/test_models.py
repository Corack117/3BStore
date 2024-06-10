import unittest
from django.test import TestCase
from applications.products.models import Product
from uuid import UUID

class ProductModelTest(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            sku='EXAMPLE-SKU-001',
            name='Jabón Zote',
            description='Barra de 200g',
            price=100,
            stock=50,
            active=True
        )
        self.assertTrue(isinstance(product, Product))
        self.assertIsNotNone(product.slug)
        self.assertIsInstance(product.slug, UUID)
        self.assertEqual(product.sku, 'EXAMPLE-SKU-001')
        self.assertEqual(product.name, 'Jabón Zote')
        self.assertEqual(product.description, 'Barra de 200g')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.stock, 50)
        self.assertTrue(product.active)
        self.assertIsNotNone(product.created)
        self.assertIsNotNone(product.updated)

    def test_unique_sku_constraint(self):
        Product.objects.create(
            sku='EXAMPLE-SKU-001',
            name='Jabón Zote',
            description='Barra de 200g',
            price=100,
            stock=50,
            active=True
        )
        with self.assertRaises(Exception):
            Product.objects.create(
                sku='EXAMPLE-SKU-001',
                name='Sal de uvas',
                description='10g',
                price=200,
                stock=100,
                active=True
            )

    def test_stock_default_value(self):
        product = Product.objects.create(
            sku='EXAMPLE-SKU-001',
            name='Jabón Zote',
            description='Barra de 200g',
            price=100
        )
        self.assertEqual(product.stock, 100)
