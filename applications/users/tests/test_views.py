import pytest
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from applications.users.models import User

@pytest.mark.usefixtures('sample_user_administrator', 'sample_user')
class UserTest(TestCase):

    @pytest.fixture(autouse=True)
    def init_fixtures(self, sample_user_administrator, sample_user):
        UserTest.sample_user_administrator = sample_user_administrator
        UserTest.sample_user = sample_user

    def create_client_instances(self):
        self.admin_client = APIClient()
        self.normal_user = APIClient()
        login_url = reverse('users-login')
        login_data = {
            'username': UserTest.sample_user_administrator.username,
            'password': 'pass123'
        }
        login_admin_response = self.admin_client.post(login_url, login_data)

        login_data = {
            'username': UserTest.sample_user.username,
            'password': 'pass123'
        }
        login_response = self.normal_user.post(login_url, login_data)

        self.admin_client.cookies = login_admin_response.cookies
        # Usuario sin privilegios
        self.normal_user.cookies = login_response.cookies

    def setUp(self):
        self.create_client_instances()

    def test_user_login(self):
        url = reverse('users-login')
        data = {
            'username': 'corack', 
            'password': 'pass123'
        }
        response = self.admin_client.post(url, data)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code , status.HTTP_200_OK)
        self.assertTrue(response_data['response'])
        self.assertEqual(response_data['data']['user']['username'] , data['username'])

    def test_user_login_fail(self):
        url = reverse('users-login')
        data = {
            'username': 'corack',
            'password': 'pass1234'
        }
        response = self.admin_client.post(url, data)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response_data['response'])

    def test_islogged(self):
        url = reverse('users-is-logged')
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        assert status_code == status.HTTP_200_OK
        self.assertTrue(response_data['response'])
        self.assertTrue(response_data['data']['isLogged'])

    def test_islogged_fail(self):
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-is-logged')
        response = client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertTrue(response_data['response'])
        self.assertFalse(response_data['data']['isLogged'])

    def test_create_user(self):
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-list')
        data = {
            "username": "armando",
            "password": "pass123",
            "email": "armando@gmail.com",
            "first_name": "Armando",
            "last_name": "Ordaz"
        }
        response = client.post(url, data)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertTrue(response_data['response'])
        self.assertEqual(response_data['data']['username'], data['username'])
        self.assertEqual(response_data['data']['last_login'], None)

    def test_create_user_repeated(self):
        # Se crea el usuario de test_create_user
        self.test_create_user()
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-list')
        data = {
            "username": "armando",
            "password": "pass123",
            "email": "armando@gmail.com",
            "first_name": "Armando",
            "last_name": "Ordaz"
        }
        response = client.post(url, data)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response_data['response'])
        self.assertEqual(response_data['data'], None)

    def test_create_user_fail(self):
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-list')
        # Se omite el campo password
        data = {
            "username": "armando",
            "email": "lalo@gmail.com",
            "first_name": "Armando",
            "last_name": "Ordaz"
        }
        response = client.post(url, data)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response_data['response']) == False
        self.assertEqual(response_data['data'], None)

    def test_get_me(self):
        url = reverse('users-me')
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertTrue(response_data['response'])
        # Usuario adminsitrador del fixture
        self.assertEqual(response_data['data']['username'], UserTest.sample_user_administrator.username)


    def test_get_me_fail(self):
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-me')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Las credenciales de autenticación no se proveyeron.")

    def test_get_all_users_like_administrator(self):
        url = reverse('users-list')
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['response'])
        self.assertIsInstance(response.data['data']['results'], list)

    def test_get_all_users_like_common_user(self):
        url = reverse('users-list')
        response = self.normal_user.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data['response'])

    def test_get_all_user_without_auth(self):
        # Cliente sin cookies (sessionid)
        client = APIClient()
        url = reverse('users-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_by_slug_like_administrator(self):
        url = reverse('users-detail', kwargs={'slug': UserTest.sample_user_administrator.slug})
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['response'])
        self.assertEqual(response.data['data']['username'], UserTest.sample_user_administrator.username)

    def test_get_user_by_slug_like_common_user(self):
        url = reverse('users-detail', kwargs={'slug': UserTest.sample_user.slug})
        response = self.normal_user.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data['response'])


    def test_get_user_by_slug_fail(self):
        url = reverse('users-detail', kwargs={'slug': 'slug-fail'})
        response = self.admin_client.get(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response_data['response'])

    def test_delete_user_like_common_user(self):
        url = reverse('users-detail', kwargs={'slug': UserTest.sample_user.slug})
        response = self.normal_user.delete(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response_data['response'])

    def test_delete_user_by_slug_like_administrator(self):
        url = reverse('users-detail', kwargs={'slug': UserTest.sample_user.slug})
        response = self.admin_client.delete(url)
        status_code = response.status_code
        response_data = response.data
        self.assertEqual(status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(response_data['response'])