from django.db import models


class Product(models.Model):

    title = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.title 
    

class Package(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class Code(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    code  = models.CharField(max_length=200)
    sold = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code