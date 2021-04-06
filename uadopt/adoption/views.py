from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Animal
from .models import Evaluation, Request
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
from accounts.forms import EvaluationForm


def index(request):
    return render(request, 'home.html')


@login_required
def adopt_a_pet(request):
    # query
    all_animals = Animal.objects.all()
    context = {'all_animals': all_animals}
    return render(request, 'adopt_a_pet.html', context)


@login_required
def adopt_a_pet(request):
    context = {}
    all_animals = Animal.objects.all()
    context['all_animals'] = all_animals
    query = request.GET.get('q')
    submitbutton = request.GET.get('submit')
    if query is not None:
        lookups = Q(p_type__icontains=query) | Q(p_name__icontains=query)
        all_animals = Animal.objects.filter(lookups).distinct()
        print(all_animals)
        context['all_animals'] = all_animals
        # context['submitbutton'] = submitbutton
        return render(request, 'adopt_a_pet.html', context)
    else:
        return render(request, 'adopt_a_pet.html', context)


@login_required
def animalInfo(request, animalId=0):
    animal_Info: object = Animal.objects.filter(id=animalId)
    animalName = animal_Info.values_list('p_name')[0][0]
    animalType = animal_Info.values_list('p_type')[0][0]
    animalImage = animal_Info.values_list('p_animalpic')[0][0]
    animalBreed = animal_Info.values_list('p_breed')[0][0]
    animalAge = animal_Info.values_list('p_age')[0][0]
    animalLocation = animal_Info.values_list('p_location')[0][0]
    animalGender = animal_Info.values_list('p_gender')[0][0]
    animalVacc = animal_Info.values_list('p_vaccination')[0][0]
    animalDesc = animal_Info.values_list('p_desc')[0][0]

    context = {'animalId': animalId,
               'animalName': animalName,
               'animalImage': animalImage,
               'animalType': animalType,
               'animalBreed': animalBreed,
               'animalAge': animalAge,
               'animalLocation': animalLocation,
               'animalGender': animalGender,
               'animalVacc': animalVacc,
               'animalDesc': animalDesc
               }
    return render(request, 'animal_info.html', context)



@login_required
def evaluation(request, animalId=-1):
    context = {
        'animalId': animalId,
    }
    userId = request.user.id
    try:
        userEvaluation = Evaluation.objects.get(user_id=userId)
    except Evaluation.DoesNotExist:
        userEvaluation = None
    form = EvaluationForm(prefix='eval', instance=userEvaluation)
    context['form'] = form

    if request.method == 'POST':
        try:
            userEvaluation = Evaluation.objects.get(user_id=userId)
        except Evaluation.DoesNotExist:
            userEvaluation = None

        form = EvaluationForm(request.POST, prefix='eval', instance=userEvaluation)

        if form.is_valid():
            update = form.save(commit=False)
            update.user_id = request.user.id
            animal = Animal.objects.get(pk=animalId)
            update.animal = animal
            form.save()
            context['form'] = form
            return redirect('../overview/' + str(animalId))

    return render(request, 'evaluation.html', context)


@login_required
def overview(request, animalId=-1):
    userId = request.user.id
    eval_id = Evaluation.objects.get(user_id=userId).id
    animalId = int(animalId)

    userInfo = User.objects.get(pk=userId)  # values('email','first_name','last_name')
    animalInfo = Animal.objects.get(pk=animalId)
    evalInfo = Evaluation.objects.get(pk=eval_id)

    context = {}
    context['userInfo'] = userInfo
    context['animalInfo'] = animalInfo
    context['evalInfo'] = evalInfo

    return render(request, 'overview.html', context)


@login_required
def requestSend(request, animalId=-1):
    currentUserId = request.user.id
    owner_id = Animal.objects.get(pk=animalId).owner_id
    req = Request(user_id=currentUserId, animal_id=animalId, admin_id=owner_id)
    req.save()
    return redirect('thankyou')


@login_required
def thankYou(request):
    message = 'Your request has been successfully send to the organization!'
    context = {'message': message}
    return render(request, 'thankyou.html', context)


def notificationList(request):
    context = {}
    return render(request, 'notificationList.html', context)


def notification(request, reqid=-1):
    context = {}
    return render(request, 'notification.html', context)


def conversationList(request):
    context = {}
    return render(request, 'conversationList.html', context)


def conversation(request, cid=-1):
    context = {}
    return render(request, 'conversation.html', context)


def aboutUs(request):
    return render(request, 'about_us.html')


def support(request):
    return render(request, 'support.html')
