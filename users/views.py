from telebot import types
from products.views import validate_request_header
from users.models import Order, User, Report
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from .models import bot

group_notification = """
السلام عليكم ورحمه الله جماعة 🌹 
لقد قمنا بفتح ڨروب تيليجرام وراح نشرحوا فيه طريقه استعمال البوت بعروض الجديده التي سوف نقدمها وباسعار جديدة :
"""
group_btn = "انضمام"
group_username = "-1002057846381"

def create_user(request):
    data = json.loads(request.body)
    user = User.objects.create(
        full_name=data['full_name'],
        balance=0,
        phone_number=data['phone_number'],
        tg_id=data['tg_id'],
        chat_id=data["chat_id"]
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
    
def new_member(request, tg_id):
    user = User.objects.get(pk=tg_id)
    user.group_member = True
    user.save()
    return JsonResponse({})


def add_to_group(request, user_id):
    user = User.objects.get(pk=user_id)
    if not user.group_member:
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(group_btn, url="https://t.me/+iB32Oft7auY1MzM0")
            )
        bot.send_message(user.chat_id,group_notification, reply_markup=markup)
    
    return redirect("/admin/users/user/")


import json

def update_order(request):
    client_message = """
    {} ترتيبك
    """
    data = json.loads(request.body)
    order = Order.objects.filter(id=data['order']).get()
    if data['status'] == Order.STATUS_CHOICES[1][0]:
        num = Order.objects.filter(status=Order.STATUS_CHOICES[1][0]).count()
        bot.send_message(order.user.chat_id, client_message.format(num))
    
    elif data['status'] == Order.STATUS_CHOICES[0][0]:
        bot.send_message(order.user.chat_id, "your order is completed")
    
    
    order.status = data['status']
    order.save()
    return JsonResponse({})

@validate_request_header
def create_report(request):
    data = json.loads(request.body)
    order = Order.objects.filter(id=data['order']).get()
    not_completed_message = "your order can't be completed bcz : {}"
    bot.send_message(
        order.user.chat_id, 
        not_completed_message.format(data['report'])
        )
    report = Report.objects.create(
        user_id=order.user.id,
        order_id=order.id,
        reason=data['report']
    )
    user = User.objects.get(pk=order.user.pk)
    user.balance += order.price
    user.save() 
    return JsonResponse({})
