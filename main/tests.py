from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from main.models import Category, Product

User = get_user_model()


# Create your tests here.
class TestProducts(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('+996555666777',
                                              'qwerty',
                                              'User1',
                                              is_active=True)
        self.admin1 = User.objects.create_superuser('+996555777888',
                                                    '123456',
                                                    'Admin1')
        self.user1_token = Token.objects.create(user=self.user1)
        self.admin1_token = Token.objects.create(user=self.admin1)
        self.category = Category.objects.create(name='Одежда', slug='clothes')
        self.product1 = Product.objects.create(name='Wind jacket',
                                               description='Warm and waterproof',
                                               category=self.category,
                                               price=5000)
        self.product2 = Product.objects.create(name='Wind jacket',
                                               description='Warm and waterproof',
                                               category=self.category,
                                               price=10000)
        self.product3 = Product.objects.create(name='Wind jacket',
                                               description='Warm and waterproof',
                                               category=self.category,
                                               price=8000)
        self.product_payload = {
            'name': 'Cool hoodie!',
            'description': 'As cool as a devil',
            'category': self.category.slug,
            'price': 1500
        }

    def test_create_product_as_anonymous_user(self):
        data = self.product_payload.copy()
        client = APIClient()
        # url = '/api/v1/products/'
        url = reverse('products-list')
        response = client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_create_product_as_simple_user(self):
        data = self.product_payload.copy()
        client = APIClient()
        # url = '/api/v1/products/'
        url = reverse('products-list')
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.user1_token.key}')
        response = client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_create_product_as_admin_user(self):
        data = self.product_payload.copy()
        client = APIClient()
        # url = '/api/v1/products/'
        url = reverse('products-list')
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin1_token.key}')
        response = client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])

    def test_create_product_without_name(self):
        data = self.product_payload.copy()
        data.pop('name')
        client = APIClient()
        url = reverse('products-list')
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin1_token.key}')
        response = client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)

    def test_get_product_details(self):
        client = APIClient()
        url = reverse('products-detail', args=(self.product1.id, ))
        response = client.get(url)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_filtering_by_price(self):
        client = APIClient()
        url = reverse('products-list')
        params = {'price_to': 8500}
        response = client.get(url, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_update_product(self):
        client = APIClient()
        url = reverse('products-detail', args=(self.product1.id, ))
        data = {'name': 'New name'}
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin1_token.key}')
        response = client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_product(self):
        client = APIClient()
        url = reverse('products-detail', args=(self.product1.id, ))
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin1_token.key}')
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
