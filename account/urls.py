from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users),
    path('users/<int:user_id>/', views.user_detail),
    path('users/change_password/', views.change_password),
    path('users/login/', views.login),
]
