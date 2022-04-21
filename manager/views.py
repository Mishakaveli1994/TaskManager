from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskCreationForm
from django.contrib import messages
from group_validation import group_required
from .models import Task


# Create your views here.
@login_required
def dashboard(request):
    user = request.user
    tasks = ''
    if user.groups.filter(name='Admin').exists():
        tasks = Task.objects.all().order_by('-updated')
    elif user.groups.filter(name='Manager').exists():
        tasks = Task.objects.all().filter(author=user.id).order_by('-updated')
    elif user.groups.filter(name='Employee').exists():
        tasks = Task.objects.all().filter(assignee=user.id).order_by('-updated')
    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard',
                   'tasks': tasks})


@group_required('Manager', 'Admin')
@login_required
def create_task(request):
    if request.method == 'POST':
        task_form = TaskCreationForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.author = request.user
            task_form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'There were problems with creating the task.')
    else:
        task_form = TaskCreationForm()
    return render(request,
                  'create_task.html',
                  {'task_form': task_form,
                   'section': 'create_task'})


@group_required('Admin')
@login_required
def administration(request):
    return render(request,
                  'administration.html',
                  {'section': 'administration'})


@login_required
def projects(request):
    return render(request,
                  'projects.html',
                  {'section': 'projects'})


def index(request):
    return render(request,
                  'index.html',
                  {'section': 'index'})
