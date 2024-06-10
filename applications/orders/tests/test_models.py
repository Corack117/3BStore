import unittest
from django.test import TestCase
from applications.orders.models import Order, OrderDetail, ProductReturn
from applications.users.models import User
from applications.products.models import Product
from uuid import UUID

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            email='test@example.com',
            first_name='John',
            last_name='Doe'
        )

        self.product_1 = Product.objects.create(
            sku='SKU001',
            name='Product 1',
            description='Description for Product 1',
            price=100,
            stock=50
        )
        self.product_2 = Product.objects.create(
            sku='SKU002',
            name='Product 2',
            description='Description for Product 2',
            price=150,
            stock=30
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            num_products=2,
            total=250
        )

        self.assertIsInstance(order, Order)
        self.assertIsNotNone(order.slug)
        self.assertIsInstance(order.slug, UUID)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.num_products, 2)
        self.assertEqual(order.total, 250)
        self.assertTrue(order.active)
        self.assertIsNotNone(order.created)
        self.assertIsNotNone(order.updated)

        order_detail_1 = OrderDetail.objects.create(
            order=order,
            product=self.product_1,
            quantity=1,
            unit_price=self.product_1.price
        )
        order_detail_2 = OrderDetail.objects.create(
            order=order,
            product=self.product_2,
            quantity=1,
            unit_price=self.product_2.price
        )

        self.assertIsInstance(order_detail_1, OrderDetail)
        self.assertIsInstance(order_detail_2, OrderDetail)
        self.assertEqual(order_detail_1.order, order)
        self.assertEqual(order_detail_2.order, order)
        self.assertEqual(order_detail_1.product, self.product_1)
        self.assertEqual(order_detail_2.product, self.product_2)
        self.assertEqual(order_detail_1.quantity, 1)
        self.assertEqual(order_detail_2.quantity, 1)
        self.assertEqual(order_detail_1.unit_price, self.product_1.price)
        self.assertEqual(order_detail_2.unit_price, self.product_2.price)