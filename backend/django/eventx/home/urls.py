from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('api/register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('api/login/', views.UserLoginView.as_view(), name='user_login'),
]