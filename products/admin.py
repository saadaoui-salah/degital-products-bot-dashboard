from django.contrib import admin
from .models import Code, Package, Product


admin.site.register(Product)
admin.site.register(Package)
admin.site.register(Code)