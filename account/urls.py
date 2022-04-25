from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeView.as_view(), name='password_change_done'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('profile/<slug:slug>', views.profile, name='profile'),
]
