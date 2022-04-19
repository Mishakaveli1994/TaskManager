from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def user_login(request):
    error_message = 'Please, use the following form to log-in:'

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
                    error_message = 'Inactive user.'
            else:
                error_message = 'Invalid Username or password'
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form,
                                                       'error_message': error_message})
