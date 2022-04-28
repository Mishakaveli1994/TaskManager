from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.index, name='index'),
    path('create_task/', views.create_task, name='create_task'),
    path('create_subtask/<int:task_id>', views.create_task, name='create_subtask'),
    path('administration/', views.administration, name='administration'),
    path('projects/', views.projects, name='projects'),
    path('tasks/tasks.json', views.tasks_listing, name='tasks-api'),
    path('tasks/<int:task_id>', views.task_details, name='task_details'),
    path('update_task/<int:task_id>', views.update_task, name='update_task'),
    path('administration', views.administration, name='administration'),
    path('assign_to_me', views.assign_to_me, name='assign_to_me'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task')
]
