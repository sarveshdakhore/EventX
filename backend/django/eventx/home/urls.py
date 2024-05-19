from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('api/register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('api/login/', views.UserLoginView.as_view(), name='user_login'),
    
    path('generate-api-key/', views.APIKeyGenerationView.as_view(), name='generate_api_key'),
    path('check-api-key/', views.check_api_key, name='check_api_key'),
]