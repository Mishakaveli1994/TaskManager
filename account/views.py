import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import Group, User


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_redirect = request.POST.get('next')
                    if not next_redirect:
                        next_redirect = 'dashboard'
                    return redirect(next_redirect)
                else:
                    messages.error(request, 'Inactive user.')
            else:
                messages.error(request, 'Invalid Username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form,
                                                       'section': 'login'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            if request.POST['password'] != request.POST['password2']:
                messages.error(request, "Passwords don't match")
                return render(request,
                              'registration/register.html',
                              {'user_form': user_form,
                               'section': 'register'})
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            my_group = Group.objects.get(name='Employee')
            my_group.user_set.add(new_user)
            Profile.objects.create(user=new_user)
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user,
                           'section': 'register'})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form,
                   'section': 'register'})


@login_required
def edit(request, slug):
    try:
        current_user = User.objects.get(username=slug)
    except ObjectDoesNotExist as e:
        return HttpResponseNotFound(f"User does not exist")
    profile_photo = ''
    if current_user.profile.photo:
        profile_photo = current_user.profile.photo.url
    if request.method == 'POST':
        user_form = UserEditForm(instance=current_user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=current_user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('edit', slug)
        else:
            messages.error(request, 'Error while updating your profile.')
    else:
        user_form = UserEditForm(instance=current_user)
        profile_form = ProfileEditForm(instance=current_user.profile)

    return render(request,
                  'registration/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'section': 'profile',
                   'profile_photo': profile_photo})


@login_required
def profile(request, slug):
    if slug:
        current_user = User.objects.get(username=slug)
    else:
        current_user = request.user
    user_profile = current_user.profile
    profile_photo = ''
    if user_profile.photo:
        profile_photo = current_user.profile.photo.url
    if request.method == 'GET':
        return render(request, 'registration/profile.html',
                      {'current_user': current_user,
                       'profile': user_profile,
                       'profile_photo': profile_photo})


@login_required
def update_user_group(request):
    if request.method == 'POST':
        try:
            values = json.loads(request.body)
            try:
                user = User.objects.get(username=values['userSlug'])
            except ObjectDoesNotExist as e:
                return HttpResponseNotFound(f"User does not exist")
            group = Group.objects.get(name=values['newGroup'])
            user.groups.clear()
            user.groups.add(group)
            user.profile.position = values['newGroup'].lower()
            user.full_clean()
            user.save()
            user.profile.full_clean()
            user.profile.save()
            payload = {'message': 'User successfully updated',
                       'status': 200}
        except Exception as e:
            print(e)
            payload = {'message': 'There was a problem with updating the user',
                       'status': 100}

        return JsonResponse(payload)
    else:
        return HttpResponseNotFound(f"Method not allowed")


@login_required
def delete_user(request):
    if request.method == 'POST':
        try:
            values = json.loads(request.body)
            try:
                user = User.objects.get(username=values['userSlug'])
            except ObjectDoesNotExist as e:
                return HttpResponseNotFound(f"User does not exist")
            user.delete()
            payload = {'message': 'User successfully deleted',
                       'status': 200}
        except Exception as e:
            print(e)
            payload = {'message': 'There was a problem with deleting the user',
                       'status': 100}

        return JsonResponse(payload)
    else:
        return HttpResponseNotFound(f"Method not allowed")

