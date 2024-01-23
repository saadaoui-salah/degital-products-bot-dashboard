from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    def __str__(self) -> str:
        return self.title 
    

class Package(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self) -> str:
        return self.name

class Code(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    code  = models.TextField()
    sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self) -> str:
        return self.code
    

@receiver(post_save, sender=Code)
def pre_save_handler(created, sender, instance, **kwargs):
    if created:
        if "\n" in instance.code:
            codes = instance.code.replace("\r",'').split("\n")
            for code in codes:
                if code != '':
                    Code.objects.create(
                        package_id=instance.package.id,
                        code = code
                        )
            instance.delete()
        else:
            instance.save()