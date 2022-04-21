from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('administration/', views.administration, name='administration'),
    path('projects/', views.projects, name='projects'),
]
