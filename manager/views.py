from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
import json
from django.db.models import Q
from .forms import TaskCreationForm
from django.contrib import messages
from group_validation import group_required
from .models import Task
from django.core.paginator import Paginator


# Create your views here.
@login_required
def dashboard(request):
    tasks_paginate_by = 10
    user = request.user
    tasks = ''
    if user.groups.filter(name='Admin').exists():
        tasks = Task.objects.all().order_by('-updated')
    elif user.groups.filter(name='Manager').exists():
        tasks = Task.objects.all().filter(author=user.id).order_by('-updated')
    elif user.groups.filter(name='Employee').exists():
        tasks = Task.objects.all().filter(assignee=user.id).order_by('-updated')
    paginator = Paginator(tasks, tasks_paginate_by)
    tasks = paginator.get_page(1)
    if request.method == 'GET':
        return render(request,
                      'dashboard.html',
                      {'section': 'dashboard',
                       'tasks': tasks})


def tasks_listing(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 11)
    user = request.user
    tasks = ''
    if user.groups.filter(name='Admin').exists():
        tasks = Task.objects.all().order_by('-updated')
    elif user.groups.filter(name='Manager').exists():
        tasks = Task.objects.all().filter(author=user.id).order_by('-updated')
    elif user.groups.filter(name='Employee').exists():
        tasks = Task.objects.all().filter(Q(assignee=None) | Q(assignee=user.id)).order_by('-updated')
    paginator = Paginator(tasks, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{'id': kw.id,
             'title': kw.title,
             'assignee': str(kw.assignee),
             'priority': kw.priority,
             'status': kw.status} for kw in
            page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)


@group_required('Manager', 'Admin')
@login_required
def create_task(request, task_id=None):
    if request.method == 'POST':
        task_form = TaskCreationForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.author = request.user
            if task_id is not None:
                new_task.parent_task = Task.objects.get(id=task_id)
            task_form.save()
            messages.success(request, 'Task created successfully!')
            return redirect(f'/tasks/{new_task.id}')
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


def about(request):
    return render(request,
                  'about.html',
                  {'section': 'about'})


@login_required
def task_details(request, task_id):
    if request.method == 'GET':
        try:
            try:
                task = Task.objects.get(id=task_id)
            except ObjectDoesNotExist as e:
                return HttpResponseNotFound(f"User does not exist")
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(f"Task {task_id} does not exist")
        subtasks = Task.objects.all().filter(parent_task=task)
        return render(request, 'task_details.html',
                      {'task': task,
                       'subtasks': subtasks})


@login_required
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except ObjectDoesNotExist as e:
        return HttpResponseNotFound(f"Task does not exist")
    if request.method == 'POST':
        try:
            task_values = json.loads(request.body)
            task.priority = task_values['priority']
            if task_values['status'] == 'in progress':
                task_values['status'] = 'in_progress'
            task.status = task_values['status']
            task.resolved = task_values['resolution']
            try:
                assignee = User.objects.get(username=task_values['assignee'])
            except ObjectDoesNotExist as e:
                return HttpResponseNotFound(f"User does not exist")
            task.assignee = assignee
            task.tracked_time = int(task_values['logged'])
            task.title = task_values['title']
            task.description = task_values['description']
            task.full_clean()
            task.save()
            payload = {'status': 'Task successfully updated'}
            return JsonResponse(payload)
        except Exception as err:
            payload = {'status': 'Task update failed',
                       'message': str(err)}
            return JsonResponse(payload)
    else:
        return HttpResponseNotFound(f"Method not allowed")


@group_required('Admin')
@login_required
def administration(request):
    users = User.objects.all().exclude(id=request.user.id)
    return render(request,
                  'administration.html',
                  {'users': users,
                   'section': 'administration'})


@group_required('Admin', 'Manager', 'Employee')
@login_required
def assign_to_me(request):
    if request.method == 'POST':
        try:
            values = json.loads(request.body)
            try:
                task = Task.objects.get(id=values['task_id'])
            except ObjectDoesNotExist as e:
                return HttpResponseNotFound(f"Task does not exist")
            if values['user_id'] == 'None':
                task.assignee = None
            else:
                try:
                    user = User.objects.get(id=values['user_id'])
                except ObjectDoesNotExist as e:
                    return HttpResponseNotFound(f"User does not exist")
                task.assignee = user
            task.save()
            if values['user_id'] == 'None':
                payload = {'message': 'Assignee removed',
                           'status': 200}
            else:
                payload = {'message': 'Task successfully assigned',
                           'status': 200}
        except Exception as e:
            print(e)
            payload = {'message': 'There was a problem with assigning the task',
                       'status': 100}

        return JsonResponse(payload)
    else:
        return HttpResponseNotFound(f"Method not allowed")


@group_required('Admin', 'Manager')
@login_required
def delete_task(request, task_id):
    try:
        try:
            task = Task.objects.get(id=task_id)
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(f"Task does not exist")
        task.delete()
        messages.success(request, 'Task deleted successfully!')
    except Exception:
        messages.error(request, 'There was a problem with deleting the task!')
    return render(request,
                  'dashboard.html',
                  {'section': 'dashboard'})
