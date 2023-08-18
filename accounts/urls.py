from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.Login.as_view(), name='login'),
  path('register/', views.Register.as_view(), name='register'),
  path('logout/', views.Logout.as_view(), name='logout'),
  path('change-profile/', views.ProfileChange.as_view(), name='change-profile'),
  path('set-password/', views.SetPassword.as_view(), name='set-password'),
]