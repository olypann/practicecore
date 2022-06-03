from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse
#from .forms import CreateUserForm
from chat.models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def choice_view(request):
    return render(request, 'accounts/choice.html')

def signup_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            # return HttpResponse('<p>Successful</p><p><a href="/logout">Sign out</a></p>')
            return render(request, 'dashboard/index.html')
    context = {'form': form}
    return render(request, 'accounts/signup.html', context=context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if not user:
            messages.info(request, 'This user doesn\'t exist')
            return render(request, 'accounts/login.html')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.info(request, 'Wrong Password')
            return render(request, 'accounts/login.html')
        login(request, user)
        return redirect('dashboard')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
