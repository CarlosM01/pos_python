from django.test import TestCase
from api.models import Product


# Create your tests here.

class ProductModelTests(TestCase):
    def setUp(self):
        self.product_data = {
            'name': 'Test Product',
            'price': 10.00,
            'stock': 100
        }
        self.product = self.create_product()

    def create_product(self):
        return Product.objects.create(**self.product_data)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 10.00)
        self.assertEqual(self.product.stock, 100)
        
    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')

    def test_check_stock_valid(self):
        self.assertTrue(self.product.check_stock(50))
        
    def test_check_stock_insufficient(self):
        with self.assertRaises(ValueError):
            self.product.check_stock(150)
            
    def test_check_stock_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.product.check_stock(0)
            
    def test_reduce_stock(self):
        initial_stock = self.product.stock
        quantity = 30
        
        self.product.reduce_stock(quantity)
        self.assertEqual(self.product.stock, initial_stock - quantity)
        
    def test_reduce_stock_insufficient(self):
        with self.assertRaises(ValueError):
            self.product.reduce_stock(150)

    def test_delete_product(self):
        initial_count = Product.objects.count()
        self.product.delete()
        self.assertEqual(Product.objects.count(), initial_count - 1)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

