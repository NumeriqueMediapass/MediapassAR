from django.urls import path
from .views import index, print_users, edit_user, create_user, delete_users

urlpatterns = [
    path('admininstration/', index, name='index_admin'),
    path('admininstration/users/', print_users, name='print_users'),
    path('admininstration/edit_user/<int:id>', edit_user, name='edit_user'),
    path('admininstration/create_user/', create_user, name='create_user'),
    path('admininstration/delete_users/', delete_users, name='delete_users'),
]