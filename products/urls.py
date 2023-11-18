from django.urls import path
from .views import *

urlpatterns = [
    path("list", get_products),
    path("pack/<str:id>", get_package_by_product),
    path("buy", buy_code),
    path("order/details/<str:pack_id>", get_order_details),
]
