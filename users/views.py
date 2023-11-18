from users.models import Order, User
from django.http import JsonResponse
import json

def create_user(request):
    data = json.loads(request.body)
    user = User.objects.create(
        full_name=data['full_name'],
        balance=0,
        phone_number=data['phone_number'],
        tg_username=data['tg_username'],
        tg_id=data['tg_id']
    )
    user.save()
    return JsonResponse({"success":"user created"})


def get_balance(request, tg_id):
    user = User.objects.filter(tg_id=tg_id)
    return JsonResponse({"balance":user.balance})


def get_details(request, tg_id):
    try:
        orders = Order.objects.filter(user__tg_id=tg_id)
        user = User.objects.filter(tg_id=tg_id).get()
        data =  {
            "pk": user.id,
            "balance": user.balance,
            "orders":0,
            "used_balance":0,
            "active": user.active,
            "full_name":user.full_name
        }
        for order in orders:
            data["orders"] += 1
            data["used_balance"] += order.package.price

        return JsonResponse(data=data)
    except Exception as e:
        print(e)
        return JsonResponse({"error":"user doesn't exist"})