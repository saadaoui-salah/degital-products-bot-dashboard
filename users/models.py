from django.db import models
from products.models import Product, Package

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=1000, decimal_places=2)
    phone_number = models.CharField(max_length=100)
    tg_username = models.CharField(unique=True, max_length=100)
    tg_id = models.CharField(unique=True, max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)