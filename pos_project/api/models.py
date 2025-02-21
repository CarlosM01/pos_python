from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    def check_stock(self, quantity):
        if quantity <= 0:
            raise ValueError(f"La cantidad debe ser mayor que 0 para {self.name}")
        if self.stock < quantity:
            raise ValueError(f"Stock insuficiente para {self.name}. Disponible: {self.stock}")
        return True

    def reduce_stock(self, quantity):
        self.check_stock(quantity)
        self.stock -= quantity
        self.save()

class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True)

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

