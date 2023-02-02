from django.urls import path
from .views import signup, login_view,logout_view, confirm_signup , confirm_signup_error

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm_signup/<token>/', confirm_signup, name='confirm_signup'),
    path('confirm_signup_error/', confirm_signup_error, name='confirm_signup_error'),
]