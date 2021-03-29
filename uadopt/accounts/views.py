from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserDetailsForm, EvaluationForm, UserPrimaryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from .models import userDetails
from adoption.models import Evaluation

from .models import userDetails


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
            messages.info(request, "Username or password incorrect")
    context = {}
    return render(request, 'login.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')


# def accountInfo(request):
#     # obj_user = get_object_or_404(User, id=request.user.id)
#     # form1 = UserDetailsForm(request.POST or None, instance=obj_user)
#     # print(obj_user)
#     # obj_user_details = get_object_or_404(userDetails, user=obj_user)
#     # form2 = UserDetailsForm_2(request.POST or None, instance=obj_user_details)
#     #
#     # obj_eval = get_object_or_404(Evaluation, user_id=request.user.id)
#     # form3 = UserDetailsForm(request.POST or None, instance=obj_eval)
#
#     # user_info = User.objects.get(id=request.user.id)
#     # form1 = UserDetailsForm(instance=user_info)
#     #
#     # # user_details = userDetails.objects.get(user=user_info)
#     # # print(user_details)
#     #
#     #
#     #
#     # context = {'form1':form1}
#     # return render(request, 'account_info.html', context)
#     pass
@login_required
def accountInfo(request):
    print(request.user.id)

    if request.method == "POST":
        form1 = UserPrimaryForm(request.POST, prefix='userInfo')
        form2 = UserDetailsForm(request.POST, prefix='userDetails')
        form3 = EvaluationForm(request.POST, prefix='eval')

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            a = form1.save()
            b = form2.save(a)
            c = form3.save(a, b)

    else:
        userId = request.user.id
        userInfo = User.objects.get(pk=userId)
        form1 = UserPrimaryForm(prefix='userInfo', instance=userInfo)
        try:
            details = userDetails.objects.get(user_id=userId)
        except userDetails.DoesNotExist:
            details = None
        form2 = UserDetailsForm(prefix='userDetails', instance=details)

        userEvaluation = get_object_or_404(Evaluation, user_id=userId)
        form3 = EvaluationForm(prefix='eval', instance=userEvaluation)

        context = {'form1': form1, 'form2': form2, 'form3': form3}
        return render(request, 'account_info.html', context)
