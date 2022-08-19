from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path('registration/', views.RegistrationView, name='registration'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),



]