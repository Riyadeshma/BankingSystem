from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('signup/', views.signup, name='signup'),
]