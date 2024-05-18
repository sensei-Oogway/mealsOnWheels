from django.urls import path
from . import views

urlpatterns = [
    path("",views.home_login),
    path('register_user', views.register_user, name='register_user'),
    path('login', views.login, name='login'),
    path('fetch_customer_profile_by_email', views.fetch_customer_profile_by_email, name='fetch_customer_profile_by_email'),
    path('edit_customer_profile', views.edit_customer_profile, name='edit_customer_profile'),
]
