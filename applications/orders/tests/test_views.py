import pytest
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from applications.orders.models import Order, OrderDetail
from applications.products.models import Product
from applications.users.models import User

@pytest.mark.usefixtures('sample_user_administrator', 'sample_user')
class OrderTest(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, sample_user_administrator, sample_user):
        OrderTest.sample_user_administrator = sample_user_administrator
        OrderTest.sample_user = sample_user

    def create_client_instances(self):
        self.admin_client = APIClient()
        self.normal_user = APIClient()
        login_url = reverse('users-login')
        login_data = {
            'username': OrderTest.sample_user_administrator.username,
            'password': 'pass123'
        }
        login_admin_response = self.admin_client.post(login_url, login_data)

        login_data = {
            'username': OrderTest.sample_user.username,
            'password': 'pass123'
        }
        login_response = self.normal_user.post(login_url, login_data)

        self.admin_client.cookies = login_admin_response.cookies
        # Usuario sin privilegios
        self.normal_user.cookies = login_response.cookies

    def setUp(self):
        self.create_client_instances()
        self.product1 = Product.objects.create(
            sku="PRODUCT-SKU-001",
            name="Producto 1",
            description="Descripción del Producto 1",
            price=1000,
            stock=100
        )
        self.product2 = Product.objects.create(
            sku="PRODUCT-SKU-002",
            name="Producto 2",
            description="Descripción del Producto 2",
            price=1500,
            stock=200
        )
        self.product3 = Product.objects.create(
            sku="PRODUCT-SKU-003",
            name="Producto 3",
            description="Descripción del Producto 3",
            price=2000,
            stock=300
        )

    def test_create_order(self):
        url = reverse('orders-list')
        data = {
            "user_id": str(OrderTest.sample_user_administrator.slug),
            "products": [
                {
                    "product_id": str(self.product1.slug),
                    "quantity": 3  
                },
                {
                    "product_id": str(self.product2.slug),
                    "quantity": 5
                },
                {
                    "product_id": str(self.product3.slug),
                    "quantity": 2
                }
            ]
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_get_orders_with_pagination(self):
        url = reverse('orders-list') + '?page=1&size=5'
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response_data['data']['results'], list))

    def test_get_order_detail(self):
        order = Order.objects.create(
            user=OrderTest.sample_user_administrator,
            num_products=10,
            total=10000
        )
        url = reverse('orders-detail', kwargs={'slug': order.slug})
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['id'], str(order.slug))

    def test_get_order_ticket(self):
        data = {
            "user_id": str(OrderTest.sample_user_administrator.slug),
            "products": [
                {
                    "product_id": str(self.product1.slug),
                    "quantity": 3  
                }
            ]
        }
        url = reverse('orders-list')
        response = self.admin_client.post(url, data, format='json')
        order_slug = response.data['data']['slug']
        url = reverse('orders-ticket', kwargs={'slug': order_slug})
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        print(response_data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['user_id'], str(OrderTest.sample_user_administrator.slug))
        self.assertTrue(isinstance(response_data['data']['products'], list))

    def test_get_order_tickets_with_pagination(self):
        url = reverse('orders-get-all-tickets') + '?page=1&size=10'
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response_data['data']['results'], list))