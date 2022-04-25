from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('administration/', views.administration, name='administration'),
    path('projects/', views.projects, name='projects'),
    path('tasks/tasks.json', views.tasks_listing, name='tasks-api'),
    path('tasks/<int:task_id>', views.task_details, name='task_details')
]
