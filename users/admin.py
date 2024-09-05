from django.contrib import admin
from django.utils import timezone
from .models import Notification, Order, Transaction, User, CreditPayment
from django.contrib.auth.models import User as CS
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.utils.html import format_html


admin.site.unregister(Group)
admin.site.unregister(CS)
admin.site.register(Notification)


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['user', 'amount', 'created_at']
    change_list_template = 'admin/transaction/change_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        current_month = timezone.now().month
        monthly_transactions = Transaction.objects.filter(created_at__month = current_month)
        earning = monthly_transactions.aggregate(total=Sum('amount'))['total']
        extra_context['monthly_stats'] = {}
        extra_context['monthly_stats']['transactions'] = monthly_transactions.count()
        extra_context['monthly_stats']['points'] = earning or 0
        return super().changelist_view(request, extra_context=extra_context)


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ['product', 'package', 'code', 'price', 'date']
    fk_name = 'user'

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1


class OrdersAdmin(admin.ModelAdmin):
    change_list_template = 'admin/orders/change_list.html'
    list_display = ['user', 'product', 'package', 'code', 'price', 'date']
    list_filter = ['status']
    search_fields =  [
        'user__full_name', 
        'user__tg_id', 
        'user__phone_number',
        'product__title',
        'package__name',
        'code__code',
        'price',
        ]
    actions = ['changelist_view']


    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        current_month = timezone.now().month
        monthly_orders = Order.objects.filter(date__month = current_month)
        earning = monthly_orders.aggregate(total=Sum('price'))['total']
        extra_context['monthly_stats'] = {}
        extra_context['monthly_stats']['points'] = earning
        extra_context['monthly_stats']['orders'] = monthly_orders.count()
        return super().changelist_view(request, extra_context=extra_context)


class UserAdmin(admin.ModelAdmin):
    inlines = [OrderInline, TransactionInline]  # Add the ItemInline to the inlines list
    list_display = [
        "full_name",
        "balance",
        "phone_number",
        "active",
        "is_admin",
        "group_member",
        "orders",
        "amount_spent_in_orders",
        "transactions",
        "total_transaction_amount",
        'add_to_group',
        'spent',
        'reset_spend'
    ]
    search_fields =  [
        'full_name', 
        'phone_number',
        'tg_id',
        ]

    def amount_spent_in_orders(self, obj):
        month = timezone.now().month 
        return Order.objects.filter(user_id=obj.id, date__month=month).aggregate(total=Sum('price'))['total'] or 0


    def orders(self, obj):
        month = timezone.now().month 
        return Order.objects.filter(user_id=obj.id, date__month=month).count()

    def transactions(self, obj):
        month = timezone.now().month 
        return Transaction.objects.filter(user_id=obj.id, created_at__month=month).count()

    def total_transaction_amount(self, obj):
        month = timezone.now().month 
        return Transaction.objects.filter(user_id=obj.id, created_at__month=month).aggregate(total=Sum('amount'))['total'] or 0

    def add_to_group(self, obj):
        if obj.group_member:
            return format_html('<button type="submit" disabled class="btn btn-primary">Group Member</button>')
        else:
            return format_html(f"""
                               <a href="/user/add-to-group/{obj.id}" class="btn btn-primary">Add To Group</a>
                               """)
    
    def reset_spend(self, obj):
        if obj.spent > 0:
            return format_html('<button type="submit" disabled class="btn btn-primary">Reset</button>')
        else:
            return format_html(f"""
                               <a href="/user/reset/{obj.id}" class="btn btn-primary">Reset</a>
                               """)

admin.site.register(User, UserAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(CreditPayment)
