from django.db import models
from products.models import Code, Package, Product
import telebot
from telebot import types
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from dirtyfields import DirtyFieldsMixin
import os

KEY = os.environ['TG_TOKEN']
bot = telebot.TeleBot(KEY, parse_mode=None)

welcome_message_2 = "• اهلأ بك عزيزي التاجر {name} 👋🏼 .\nنحن هنا لنوفر لكم كل منتجات جملة بأفضل اسعار 🤩\nمعلوماتك {pk}\nنقاطك   {balance}\n• قم بأختيار القسم الذي تريده من الاسفل 👇🏽."

balance_btn = "💰 رصيدي"
products_btn = "🛒 العروض التي يقدمها البوت"
ask_for_balance_btn = "💵 شحن حسابي"
contact_us_btn = "☎️ تواصل معنا"
history_btn = "📋 تعاملاتي"
buy_btn = "شراء"


class User(DirtyFieldsMixin, models.Model):
    full_name = models.CharField(max_length=200)
    balance = models.IntegerField()
    phone_number = models.CharField(max_length=100)
    tg_id = models.CharField(unique=True, max_length=100)
    chat_id = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    group_member = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.tg_id} || {self.full_name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Done', 'DONE'),
        ('In Progress', 'IN PROGRESS'),
        ('Not Started', 'NOT STARTED'),
        ('Have Problems', 'HAVE PROBLEMS'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="admin_user", limit_choices_to={'is_admin': True})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    code = models.ForeignKey(Code, on_delete=models.CASCADE, null=True, blank=True)
    extra = models.CharField(max_length=500, null=True, blank=True)
    price = models.IntegerField()
    date = models.DateTimeField()
    status = models.CharField(max_length=500, choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.full_name} || {self.code.code if self.code else ''}"

class Notification(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user} recived {self.amount} points"

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()

    def __str__(self) -> str:
        return f"{self.user}"



@receiver(post_save, sender=Notification)
def pre_save_handler(created, sender, instance, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            if user.chat_id != "1045530860":
                try:
                    bot.send_message(user.chat_id, instance.text)
                    print("--------- Notification sent ---------")
                except Exception as e: 
                    print(e)


order_message = """
New order created 
    
    Order id: {order_id}
    package: {package}
    user id: {user_id} || {user_name}
    request text: {request_text}

"""

strat_btn = "ابدء"
reject_btn = "لن نستطيع"

@receiver(post_save, sender=Order)
def pre_save_handler(created, sender, instance, **kwargs):
    if created:
        users = User.objects.filter(is_admin=True)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(strat_btn, callback_data=f"order_status=start&order_id={instance.id}"),
            types.InlineKeyboardButton(reject_btn, callback_data=f"order_status=reject&order_id={instance.id}")
        )
        for user in users:
            message = order_message.format(
                order_id=instance.id, 
                package=instance.package.name,
                user_id=instance.user.tg_id,
                user_name=instance.user.full_name,
                request_text=instance.extra
                )
            try:
                bot.send_message(user.chat_id, message, reply_markup=markup)
                print("--------- Notification sent ---------")
            except Exception as e: 
                print(e)


@receiver(pre_save, sender=User)
def pre_save_handler(sender, instance, **kwargs):
    # Check if 'field_to_update' is being updated
    try:
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(balance_btn),
            types.InlineKeyboardButton(products_btn)
        )
        markup.add(
            types.InlineKeyboardButton(ask_for_balance_btn),
            types.InlineKeyboardButton(contact_us_btn),
        )
        markup.add(
            types.InlineKeyboardButton(history_btn)
        )
        if 'active' in instance.get_dirty_fields() and instance.active and instance.is_dirty():
            bot.send_message(instance.chat_id, "لقد تم قبول طلبك")
            bot.send_message(
                instance.chat_id, 
                welcome_message_2.format(
                    pk=instance.tg_id,
                    name=instance.full_name,
                    balance=instance.balance
                    ), 
                reply_markup=markup)
        if 'balance' in instance.get_dirty_fields() and instance.get_dirty_fields()['balance'] < instance.balance and instance.is_dirty():
            bot.send_message(instance.chat_id, 
                f"تم اضافة {instance.balance - int(instance.get_dirty_fields()['balance'])} نقطة إلى حسابك الآن ."
                )
            bot.send_message(
                instance.chat_id, 
                welcome_message_2.format(
                    pk=instance.tg_id,
                    name=instance.full_name,
                    balance=instance.balance
                    ), 
                reply_markup=markup)
    except Exception as e :
        print(e)


@receiver(post_save, sender=Transaction)
def pre_save_handler(created, sender, instance, **kwargs):
    if created:
        instance.user.balance += instance.amount
        instance.user.save()
        instance.save()