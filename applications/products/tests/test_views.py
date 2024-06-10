import pytest
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from applications.products.models import Product

@pytest.mark.usefixtures('sample_user_administrator', 'sample_user')
class ProductTest(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, sample_user_administrator, sample_user):
        ProductTest.sample_user_administrator = sample_user_administrator
        ProductTest.sample_user = sample_user

    def create_client_instances(self):
        self.admin_client = APIClient()
        self.normal_user = APIClient()
        login_url = reverse('users-login')
        login_data = {
            'username': ProductTest.sample_user_administrator.username,
            'password': 'pass123'
        }
        login_admin_response = self.admin_client.post(login_url, login_data)

        login_data = {
            'username': ProductTest.sample_user.username,
            'password': 'pass123'
        }
        login_response = self.normal_user.post(login_url, login_data)

        self.admin_client.cookies = login_admin_response.cookies
        # Usuario sin privilegios
        self.normal_user.cookies = login_response.cookies

    def setUp(self):
        self.create_client_instances()
        self.product = Product.objects.create(
            sku="EXAMPLE-SKU-001",
            name="Aceite de oliva Mar Amargo",
            description="Aceite de oliva marca Mar Amargo, tamaño 500ml",
            price=1530,
            stock=15
        )

    def test_create_product(self):
        url = reverse('products-list')
        data = {
            "sku": "EXAMPLE-SKU-002",
            "name": "Nuevo producto",
            "description": "Descripción del nuevo producto",
            "price": 2000,
            "stock": 10
        }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_get_products_with_pagination(self):
        url = reverse('products-list') + '?page=1&size=5'
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response_data['data']['results'], list))

    def test_get_product_detail(self):
        url = reverse('products-detail', kwargs={'sku': self.product.sku})
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['sku'], self.product.sku)

    def test_update_product(self):
        url = reverse('products-detail', kwargs={'sku': self.product.sku})
        data = {
            "sku": "EXAMPLE-SKU-001",
            "name": "Aceite de oliva Mar Amargo",
            "description": "Aceite de oliva marca Mar Amargo, tamaño 500ml",
            "stock": 14,
            "price": 15
        }
        response = self.admin_client.put(url, data, format='json')
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['stock'], 14)

    def test_partial_update_product(self):
        url = reverse('products-detail', kwargs={'sku': self.product.sku})
        data = {
            "stock": 11
        }
        response = self.admin_client.patch(url, data, format='json')
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['data']['stock'], 11)

    def test_delete_product(self):
        url = reverse('products-detail', kwargs={'sku': self.product.sku})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.filter(active=True).count(), 0)

    def test_add_to_inventory(self):
        url = reverse('add-to-inventory', kwargs={'sku': self.product.sku})
        data = {
            "add_to_stock": 14
        }
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.first().stock, 29)
