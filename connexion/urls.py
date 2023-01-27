from django.urls import path
from .views import signup, login_view, acceuil, logout_view

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('',acceuil, name='acceuil'),
    path('logout/', logout_view, name='logout'),
]