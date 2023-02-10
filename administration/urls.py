from django.urls import path
from .views import index, print_users, edit_user, create_user, delete_users, create_mediatheque, get_mediatheques,\
     edit_mediatheque, delete_mediatheque

urlpatterns = [
    path('admininstration/', index, name='index_admin'),
    path('admininstration/users/', print_users, name='print_users'),
    path('admininstration/edit_user/<int:id>', edit_user, name='edit_user'),
    path('admininstration/create_user/', create_user, name='create_user'),
    path('admininstration/delete_users/', delete_users, name='delete_users'),
    path('admininstration/create_mediatheque/', create_mediatheque, name='create_mediatheque'),
    path('admininstration/mediatheques/', get_mediatheques, name='get_mediatheques'),
    path('admininstration/edit_mediatheque/<int:id>', edit_mediatheque, name='edit_mediatheque'),
    path('admininstration/delete_mediatheque/', delete_mediatheque, name='delete_mediatheque'),
]