from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from adoption.models import Request, Evaluation, Animal

from .forms import CreateAdminUserForm, OrgForm, CreateOrgForm, CreatePetForm
from .models import AdminPanel
from accounts.forms import UserPrimaryForm, UserDetailsForm
from accounts.models import userDetail


def adminIndex(request):
    return render(request, 'admin_home.html')


@login_required
def accountInfo(request):
    print(request.user.id)
    user = request.user
    if request.method == "POST":
        userId = request.user.id
        try:
            userInfo = User.objects.get(pk=userId)
        except:
            userInfo = None
        form1 = UserPrimaryForm(request.POST or None, prefix='userInfo', instance=userInfo)

        try:
            details = userDetail.objects.get(user_id=userId)
        except:
            details = None
        form2 = UserDetailsForm(request.POST or None, prefix='userDetails', instance=details)

        try:
            orgDetails = AdminPanel.objects.get(user=user)
        except:
            orgDetails = None

        form3 = OrgForm(request.POST or None, prefix='eval', instance=orgDetails)

        if form1.is_valid() and form2.is_valid() and form3.is_valid():
            print("Admin : All forms are cleared")
            form1.save()

            update = form2.save(commit=False)
            update.user_id = request.user.id
            form2.save()

            update = form3.save(commit=False)
            update.user_id = request.user.id
            form3.save()
            context = allDetails(request)
            return render(request, 'admin_account_info.html', context)
        context = allDetails(request)
        return render(request, 'admin_account_info.html', context)

    else:
        context = allDetails(request)
        return render(request, 'admin_account_info.html', context)


def allDetails(request):
    userId = request.user.id
    user = request.user
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
        orgDetails = AdminPanel.objects.get(user=user)
    except Evaluation.DoesNotExist:
        orgDetails = None
    form3 = OrgForm(prefix='eval', instance=orgDetails)

    context = {'form1': form1, 'form2': form2, 'form3': form3}
    return context


def adminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        admin = AdminPanel.objects.get(user=user)
        if admin.is_admin == True:
            print("Logged in as Admin", user.id)
            login(request, user)
            return redirect('adminIndex')
        else:
            print("I am not an admin")
            messages.info(request, "Username or password incorrect")
    context = {}

    return render(request, 'admin_login.html')


def adminRegister(request):
    form = CreateAdminUserForm()
    form2 = CreateOrgForm()
    if request.method == 'POST':
        form = CreateAdminUserForm(request.POST)
        form2 = CreateOrgForm(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            print("saving")
            user = form.cleaned_data.get('username')
            messages.success(request, 'The Account was created successfully for ' + user)
            form.save()
            user_ = User.objects.get(username=user)
            print(type(user))
            admin = AdminPanel.objects.get(user=user_)
            admin.is_admin = True
            admin.org_name = request.POST['org_name']
            admin.org_phone = request.POST['org_phone']
            admin.org_address = request.POST['org_address']
            admin.org_city = request.POST['org_city']
            admin.org_state = request.POST['org_state']
            admin.org_zipcode = request.POST['org_zipcode']

            admin.org_doc = request.FILES['org_doc']

            admin.save()

            return redirect('login')
    print('Not Saving')
    context = {'form': form, 'form2': form2}
    return render(request, 'admin_registration.html', context)


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
    # initial_dict = {
    #     'owner_id' : request.user.id,
    # }
    form = CreatePetForm()
    if request.method == 'POST':
        form = CreatePetForm(request.POST, request.FILES)
        # form.owner_id = request.user.id
        if form.is_valid():
            update = form.save(commit=False)
            update.owner_id = request.user.id
            form.save()
            return redirect('pets')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")

    else:
        return render(request, 'add-pet.html', {'form': form})


@login_required
def modifyPets(request, animalId):
    print("Animal id : ", animalId)
    context = {'animalId': animalId}
    obj = get_object_or_404(Animal, id=animalId)
    form = CreatePetForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        # return render(request, "modify-pet.html", context)

    # add form dictionary to context
    context["form"] = form

    return render(request, "modify-pet.html", context)


@login_required
def deletePets(request, animalId):
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Animal, id=animalId)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("pets")

    return render(request, "delete-pet.html", context)


@login_required
def viewQuestions(request):
    pass


@login_required
def giveResponse(request):
    pass
