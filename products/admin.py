from django.contrib import admin
from django.db.models import Sum
from users.models import Order
from .models import Code, Package, Product
from django.utils import timezone


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['title', 'orders', 'points']

    def orders(self, obj):
        month = timezone.now().month
        return Order.objects.filter(product_id=obj.id, date__month=month).count()

    def points(self, obj):
        month = timezone.now().month
        return Order.objects.filter(product_id=obj.id, date__month=month).aggregate(total=Sum('price'))['total'] or 0

class PackageAdmin(admin.ModelAdmin):
    model = Package
    list_display = ['name', 'orders', 'points']

    def orders(self, obj):
        month = timezone.now().month
        return Order.objects.filter(package_id=obj.id, date__month=month).count()

    def points(self, obj):
        month = timezone.now().month
        return Order.objects.filter(package_id=obj.id, date__month=month).aggregate(total=Sum('price'))['total'] or 0


class CodeAdmin(admin.ModelAdmin):
    model = Code
    list_display = ['code', 'sold']




admin.site.register(Product, ProductAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Code, CodeAdmin)