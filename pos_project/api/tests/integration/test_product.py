from rest_framework import status
from rest_framework.test import APITestCase
from ...models import Product

class ProductAPITests(APITestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Test Product',
            'price': 10.00,
            'stock': 100
        }
        # Crear un producto para los tests que necesitan uno existente
        self.product = Product.objects.create(**self.product_data)
        
    def test_create_product_api(self):
        new_product_data = {
            'name': 'New Product',
            'price': 15.00,
            'stock': 50
        }
        response = self.client.post('/api/products/', new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.last().name, 'New Product')

    def test_get_product_api(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product_api(self):
        updated_data = {
            'name': 'Updated Product',
            'price': 15.00,
            'stock': 80
        }
        response = self.client.put(
            f'/api/products/{self.product.id}/',
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_delete_product_api(self):
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_invalid_data(self):
        invalid_product_data = {
            'name': '',  # empty name should be invalid
            'price': -10.00,  # negative price should be invalid
            'stock': -5  # negative stock should be invalid
        }
        response = self.client.post('/api/products/', invalid_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Product.objects.count(), 1)  # no new product should be created

    def test_get_product_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')

    def test_get_nonexistent_product(self):
        response = self.client.get('/api/products/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
