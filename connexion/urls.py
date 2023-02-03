from django.urls import path
from .views import signup, login_view,logout_view, confirm_signup , confirm_signup_error
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm_signup/<token>/', confirm_signup, name='confirm_signup'),
    path('confirm_signup_error/', confirm_signup_error, name='confirm_signup_error'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='connexion/password_reset.html'), name = 'password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='connexion/password_reset_done.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='connexion/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='connexion/password_reset_complete.html'), name='password_reset_complete'),
]