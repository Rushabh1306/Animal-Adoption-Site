from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse

from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from adoption.models import Request, Evaluation, Animal

from .models import AdminPanel


def adminIndex(request):
    return render(request, 'admin_home.html')


def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            admin = AdminPanel.objects.get(user=user)
            print("Logged in as Admin", user.id)
            login(request, user)
            return redirect('adminIndex')
        except:
            print("I am not an admin")
            messages.info(request, "Username or password incorrect")
    context = {}

    return render(request, 'admin_login.html')


def adminRegister(request):
    return render(request, 'admin_registration.html')


def adminLogoutUser(request):
    logout(request)
    return redirect('/')


@login_required
def viewRequest(request):
    currentAdminId = request.user.id
    print("Current Admin Id:", currentAdminId)
    requestInfo = Request.objects.filter(admin_id=currentAdminId, status='pending')
    try:
        print(requestInfo[0].user_id)
    except:
        return HttpResponse('No Requests has been directed to your organization')
    data = []
    for req in requestInfo:
        ind = []
        userId = req.user_id
        userInfo = User.objects.get(pk=userId)
        userName = userInfo.first_name + ' ' + userInfo.last_name
        userEmail = userInfo.email

        animalId = req.animal_id
        animalInfo = Animal.objects.get(pk=animalId)

        ind = {
            'reqid': req.id,
            'animalpic': animalInfo.p_animalpic,
            'animalName': animalInfo.p_name,
            'userName': userName,
            'userEmail': userEmail}
        data.append(ind)

    context = {'data': data}
    return render(request, 'view_request.html', context)


@login_required
def viewRequestInfo(request, reqid=-1):
    req = Request.objects.get(pk=reqid)
    userId = req.user_id
    animalId = req.animal_id
    eval_id = Evaluation.objects.get(user_id=userId).id
    userInfo = User.objects.get(pk=userId)  # values('email','first_name','last_name')
    animalInfo = Animal.objects.get(pk=animalId)
    evalInfo = Evaluation.objects.get(pk=eval_id)

    context = {}
    context['userInfo'] = userInfo
    context['animalInfo'] = animalInfo
    context['evalInfo'] = evalInfo
    context['reqid'] = reqid

    return render(request, 'view_request_info.html', context)


@login_required
def confirmRequest(request, reqid=-1):
    req = Request.objects.get(pk=reqid)
    req.status = 'approved'
    req.save()
    return render(request, 'confirm_request.html')


@login_required
def rejectedRequest(request, reqid=-1):
    req = Request.objects.get(pk=reqid)
    req.status = 'rejected'
    req.save()
    return render(request, 'view_request_info.html')


@login_required
def pets(request):
    currentuserId = request.user.id
    allAnimals = Animal.objects.filter(owner_id=currentuserId)
    context = {'all_animals': allAnimals}
    return render(request, 'pets.html',context)


@login_required
def addPets(request):
    pass


@login_required
def modifyPets(request):
    pass


@login_required
def deletePets(request):
    pass


@login_required
def viewQuestions(request):
    pass

@login_required
def giveResponse(request):
    pass
