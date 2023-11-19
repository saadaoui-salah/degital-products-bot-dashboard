from django.db import models
from products.models import Product, Package
import telebot
from telebot import types
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from dirtyfields import DirtyFieldsMixin

KEY = "6852207591:AAH9CEoxLGFmo_OhwXK2ai-rgPHPEvXqYrw"
bot = telebot.TeleBot(KEY, parse_mode=None)

welcome_message_2 = "• اهلأ بك عزيزي التاجر {name} 👋🏼 .\nنحن هنا لنوفر لكم كل منتجات جملة بأفضل اسعار 🤩\nمعلوماتك {pk}\nنقاطك   {balance}\n• قم بأختيار القسم الذي تريده من الاسفل 👇🏽."

balance_btn = "💰 رصيدي"
products_btn = "🛒 العروض التي يقدمها البوت"
ask_for_balance_btn = "💵 شحن حسابي"
contact_us_btn = "☎️ تواصل معنا"
history_btn = "📋 تعاملاتي"
buy_btn = "شراء"


# Create your models here.
class User(DirtyFieldsMixin, models.Model):
    full_name = models.CharField(max_length=200)
    balance = models.IntegerField()
    phone_number = models.CharField(max_length=100)
    tg_username = models.CharField(unique=True, max_length=100)
    tg_id = models.CharField(unique=True, max_length=100)
    chat_id = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.tg_id} || {self.full_name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)


class Notification(models.Model):
    text = models.TextField()

    def __str__(self) -> str:
        return self.text

@receiver(post_save, sender=Notification)
def pre_save_handler(created, sender, instance, **kwargs):
    if created:
        users = User.objects.all()
        for user in users:
            bot.send_message(user.chat_id, instance.text)


@receiver(pre_save, sender=User)
def pre_save_handler(sender, instance, **kwargs):
    # Check if 'field_to_update' is being updated
    if 'active' in instance.get_dirty_fields() and instance.active and instance.is_dirty():
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
        bot.send_message(instance.chat_id, "لقد تم قبول طلبك")
        bot.send_message(
            instance.chat_id, 
            welcome_message_2.format(
                pk=instance.pk,
                name=instance.full_name,
                balance=instance.balance
                ), 
            reply_markup=markup)

