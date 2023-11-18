from django.urls import path
from .views import *

urlpatterns = [
    path('create', create_user),
    path('details/<str:tg_id>', get_details),
    path('balance/<str:tg_id>', get_balance)
]
