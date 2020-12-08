from decimal import Decimal

from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse, path, include
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import APIClient

from core.models import Product

from ApiDockerBasicCrud.urls import router


class ProductCreateApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

    def test_create_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        data = {
            'name': 'Botina',
            'description': 'Botina de couro argentina',
            'value': 299.99,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Botina')

    def test_validate_wrong_value_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        data = {
            'name': 'Botina',
            'description': 'Botina de couro argentina',
            'value': 299.999,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

    def test_validate_wrong_name_len_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        data = {
            'name': 'Botina',
            'description': 'Botina de couro argentina',
            'value': 2222222299.99,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

    def test_validate_wrong_value_string_len_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        data = {
            'name': 'Botinaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'description': 'Botina de couro argentina',
            'value': 299.99,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 0)

class ProductUpdateApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.product = Product.objects.create(
            name='Botina',
            description='Botina de couro bonita',
            value=299.99)

        self.TWOPLACES = Decimal(10) ** -2

    def test_update_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[1])
        data = {
            'name': 'Bota',
            'description': 'Botina de couro argentina',
            'value': 199.99,
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Bota')
        self.assertEqual(Product.objects.get().description, 'Botina de couro argentina')
        self.assertEqual(Product.objects.get().value, Decimal(199.99).quantize(self.TWOPLACES))


class ProductPatchApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.product = Product.objects.create(
            name='Botina',
            description='Botina de couro bonita',
            value=299.99)

        self.TWOPLACES = Decimal(10) ** -2

    def test_patch_product_value(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[1])
        data = {
            'value': 199.99,
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Botina')
        self.assertEqual(Product.objects.get().description, 'Botina de couro bonita')
        self.assertEqual(Product.objects.get().value, Decimal(199.99).quantize(self.TWOPLACES))

    def test_patch_product_description(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[1])
        data = {
            'description': 'Descrição alterada',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Botina')
        self.assertEqual(Product.objects.get().description, 'Descrição alterada')
        self.assertEqual(Product.objects.get().value, Decimal(299.99).quantize(self.TWOPLACES))

    def test_patch_product_name(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[1])
        data = {
            'name': 'Bota',
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Bota')
        self.assertEqual(Product.objects.get().description, 'Botina de couro bonita')
        self.assertEqual(Product.objects.get().value, Decimal(299.99).quantize(self.TWOPLACES))


class ProductGetApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.product = Product.objects.create(
            name='Botina',
            description='Botina de couro bonita',
            value=299.99)

        self.product2 = Product.objects.create(
            name='Botina2',
            description='Botina2 de couro bonita',
            value=499.99)

        self.TWOPLACES = Decimal(10) ** -2

    def test_get_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=self.product.id).name, response.data['name'])
        self.assertEqual(Product.objects.get(id=self.product.id).description, response.data['description'])

    def test_get_products(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())
        self.assertEqual(Product.objects.first().name, response.data[0]['name'])
        self.assertEqual(Product.objects.last().name, response.data[-1]['name'])


class ProductDeleteApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.product = Product.objects.create(
            name='Botina',
            description='Botina de couro bonita',
            value=299.99)

        self.product2 = Product.objects.create(
            name='Botina2',
            description='Botina2 de couro bonita',
            value=499.99)

        self.TWOPLACES = Decimal(10) ** -2

    def test_delete_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[self.product.id])

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)



    def test_delete_2_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[self.product.id])
        url2 = reverse('product-detail', args=[self.product2.id])

        response = self.client.delete(url, format='json')
        response2 = self.client.delete(url2, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('', include(router.urls)),
        path('api-auth/', include('rest_framework.urls')),
        path('admin/', admin.site.urls),
    ]

    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@mundodevops.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.product = Product.objects.create(
            name='Botina',
            description='Botina de couro bonita',
            value=299.99)

        self.product2 = Product.objects.create(
            name='Botina2',
            description='Botina2 de couro bonita',
            value=499.99)

    def test_list_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_detail_product(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)