from users.models import Order, User
from .models import Product, Package, Code
from django.core.serializers import serialize
from django.http import JsonResponse


def get_products(request):
    products = Product.objects.all()
    data = serialize('json', products)
    return JsonResponse(data, safe=False)


def get_package_by_product(request, id):
    packs = Package.objects.filter(product_id=id).order_by('-id')
    data = []
    for pack in packs:
        data.append({
            "id": pack.id,
            "name": pack.name,
            "price": pack.price,
            "count": Code.objects.filter(package_id=pack.id, sold=False).count(),
        })
    return JsonResponse(data, safe=False)

def get_order_details(request, pack_id):
    pack = Package.objects.get(pk=pack_id) 
    code_count = Code.objects.filter(sold=False, package_id=pack_id).count()
    data = {
        "title": pack.name,
        "description": pack.product.title,
        "price": pack.price,
        "count": code_count
    }
    return JsonResponse(data, safe=False)

import json

def buy_code(request):
    data = json.loads(request.body)
    code = Code.objects.filter(package_id=data['pack_id'], sold=False).first()
    code.sold = True
    pack = Package.objects.filter(id=data['pack_id']).get()
    user = User.objects.filter(tg_id=data['tg_id']).get() 
    if user.balance >= pack.price: 
        user.balance -= pack.price 
        order = Order.objects.create(
            user_id=user.id,
            package_id=pack.id, 
            code_id=code.id,
            product_id=pack.product.id,
            price = pack.price
        )
        order.save()
        code.save()
        user.save()
        data = {
            "code": code.code, 
            "price": pack.price,
            "user": user.full_name,
            "pack": pack.name,
            "product": pack.product.title
            }
        return JsonResponse(data=data)
    else: 
        return JsonResponse({"error": "404"})

