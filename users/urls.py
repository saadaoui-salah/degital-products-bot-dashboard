from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_user),
    path('details/<str:tg_id>', get_details),
    path('balance/<str:tg_id>', get_balance),
    path('new_member/<str:tg_id>', get_balance),
    path("add-to-group/<str:user_id>", add_to_group),
    path("update-order", update_order),
    path("report", create_report),
]
