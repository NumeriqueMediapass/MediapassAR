from django.urls import path
from .views import index, print_users

urlpatterns = [
    path('admininstration/', index, name='index_admin'),
    path('admininstration/users/', print_users, name='print_users'),
]