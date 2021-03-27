from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Animal
from .models import Evaluation, Request
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'home.html')

@login_required
def adopt_a_pet(request):
    # query
    all_animals = Animal.objects.all()
    context = {'all_animals': all_animals}
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
        'animalId': animalId
    }
    print(animalId)
    if request.method == 'POST':
        print('In Post Method')
        q1 = request.POST.get('answer1')
        currentUserId = request.user.id
        print(q1,animalId)
        animal = Animal.objects.get(pk=animalId)
        if checkEval(currentUserId):
            print('Updated')
            eval = Evaluation.objects.get(user_id=currentUserId)
            Evaluation.objects.filter(pk=eval.id).update(evaluation_details=q1,animal=animal)
        else:
            print('New')
            newEval = Evaluation(user_id=currentUserId, evaluation_details=q1,animal=animal)
            newEval.save()
        return redirect('../overview')
    else:
        return render(request, 'evaluation.html', context)


def checkEval(userId):
    if Evaluation.objects.filter(user_id=userId):
        return True
    return False

@login_required
def overview(request):


    userId = request.user.id
    eval_id = Evaluation.objects.get(user_id=userId).id
    animalId = Evaluation.objects.get(user_id=userId).animal_id

    userInfo = User.objects.get(pk=userId) # values('email','first_name','last_name')
    animalInfo = Animal.objects.get(pk=animalId)

    evalInfo = Evaluation.objects.get(pk=eval_id)
    # print('UserInfo : ', userInfo.password)
    # print('AnimalInfo : ', animalInfo)
    # print('EvalInfo : ', evalInfo)
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


def notifications(request):
    pass


def aboutUs(request):
    return render(request, 'about_us.html')


def support(request):
    return render(request, 'support.html')