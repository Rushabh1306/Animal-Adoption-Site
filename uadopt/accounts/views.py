from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print("saving")
            user = form.cleaned_data.get('username')
            messages.success(request, 'The Account was created successfully for ' + user)
            form.save()
            return redirect('login')
    print('Not Saving')
    context = {'form': form}
    return render(request, 'registration.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Username or password incorrect")
    context = {}
    return render(request, 'login.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')


