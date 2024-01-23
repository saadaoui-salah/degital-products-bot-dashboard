from django.contrib import admin
from .models import Notification, Order, User
from django.contrib.auth.models import User as CS
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.unregister(Group)
admin.site.unregister(CS)
admin.site.register(Notification)

admin.site.register(Order)