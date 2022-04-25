from django import forms
from .models import Task


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'estimate']


class SubTaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'parent_task', 'priority', 'estimate']


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title',
                  'description',
                  'author',
                  'assignee',
                  'status',
                  'priority',
                  'estimate',
                  'parent_task',
                  'publish',
                  'tracked_time']
