from functools import wraps
from django.utils import timezone
from users.models import Order, User
from .models import Product, Package, Code
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest, JsonResponse

def validate_request_header(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Get the value of the specified header from the request
        header_value = request.headers.get("User")

        # Check if the header is present and has the expected value
        valid_user = User.objects.filter(chat_id=header_value, active=True).exists()
        if header_value is None or not valid_user:
            print(valid_user, header_value)
            return HttpResponseBadRequest(f"Invalid or missing User header")

        # Call the original view function if the header is valid
        return view_func(request, *args, **kwargs)

    return wrapped_view


@validate_request_header
def get_products(request):
    products = Product.objects.all()
    data = serialize('json', products)
    return JsonResponse(data, safe=False)

@validate_request_header
def get_package_by_product(request, id):
    packs = Package.objects.filter(product_id=id).order_by('-id')
    data = []
    for pack in packs:
        if pack.choices == Package.CHOICES[0][0]:
            count = Code.objects.filter(package_id=pack.id, sold=False).count()
        else:
            count = 'عند الطلب'
        data.append({
            "id": pack.id,
            "name": pack.name,
            "price": pack.price,
            "count": count,

        })
    return JsonResponse(data, safe=False)

def get_order_details(request, pack_id):
    pack = Package.objects.get(pk=pack_id) 
    count = ''
    description = None
    if pack.choices == Package.CHOICES[0][0]:
        count = Code.objects.filter(package_id=pack.id, sold=False).count()
    else:
        count = 'عند الطلب'
    if pack.description:
        description = pack.description.format(price=pack.price, name=pack.name, count=count)
    elif pack.product.description:
        description = pack.product.description.format(price=pack.price, name=pack.name, count=count)
    data = {
        "title": pack.name,
        "description": pack.product.title,
        "price": pack.price,
        "count": count,
        "description": description,
        "image": pack.image.url or pack.product.image.url if pack.image else None,

    }
    return JsonResponse(data, safe=False)

import json

@validate_request_header
def buy_code(request):
    data = json.loads(request.body)
    code = Code.objects.filter(package_id=data['pack_id'], sold=False).first()
    pack = Package.objects.filter(id=data['pack_id']).get()
    user = User.objects.filter(tg_id=data['tg_id']).get()          
    if user.balance >= pack.price: 
        code.sold = True
        user.balance -= pack.price 
        order = Order.objects.create(
            user_id=user.id,
            package_id=pack.id, 
            code_id=code.id,
            product_id=pack.product.id,
            price = pack.price, 
            date = timezone.now() 
        )
        if pack.choices == Package.CHOICES[0][0]:
            order.status = Order.STATUS_CHOICES[2][0]
            order.extra = data.get('extra')

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
        if pack.choices == Package.CHOICES[1][0]:
            data['order'] = Order.objects.filter(status=Order.STATUS_CHOICES[1][0])
        return JsonResponse(data=data)
    else: 
        return JsonResponse({"error": "404"})