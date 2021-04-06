from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserDetailsForm, EvaluationForm, UserPrimaryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from adoption.models import Evaluation

from .models import userDetail


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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Username or password incorrect")
    context = {}
    return render(request, 'login.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')


# AccountInfo
@login_required
def accountInfo(request):
    print(request.user.id)

    if request.method == "POST":
        userId = request.user.id
        try:
            userInfo = User.objects.get(pk=userId)
        except:
            userInfo = None
        form1 = UserPrimaryForm(request.POST, prefix='userInfo', instance=userInfo)

        try:
            details = userDetail.objects.get(user_id=userId)
        except userDetail.DoesNotExist:
            details = None
        form2 = UserDetailsForm(request.POST, prefix='userDetails', instance=details)

        try:
            userEvaluation = Evaluation.objects.get(user_id=userId)
        except Evaluation.DoesNotExist:
            userEvaluation = None

        form3 = EvaluationForm(request.POST, prefix='eval', instance=userEvaluation)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            print("All forms are cleared")
            form1.save()

            update = form2.save(commit=False)
            update.user_id = request.user.id
            form2.save()

            update = form3.save(commit=False)
            update.user_id = request.user.id
            form3.save()
        context = allDetails(request)
        return render(request, 'account_info.html', context)

    else:
        context = allDetails(request)
        return render(request, 'account_info.html', context)


def allDetails(request):
    userId = request.user.id
    # user primary details
    userInfo = User.objects.get(pk=userId)
    form1 = UserPrimaryForm(prefix='userInfo', instance=userInfo)
    # # user details
    try:
        details = userDetail.objects.filter(user_id=userId).first()
    except userDetail.DoesNotExist:
        details = None
    form2 = UserDetailsForm(prefix='userDetails', instance=details)

    # user evaluation
    try:
        userEvaluation = Evaluation.objects.get(user_id=userId)
    except Evaluation.DoesNotExist:
        userEvaluation = None
    form3 = EvaluationForm(prefix='eval', instance=userEvaluation)

    context = {'form1': form1, 'form2': form2, 'form3': form3}
    return context
