from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import userDetail
from adoption.models import Evaluation


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserPrimaryForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserDetailsForm(ModelForm):
    class Meta:
        model = userDetail
        fields = ['phone_number', 'address', 'city', 'state', 'zipcode']


class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'answer6', 'answer7', 'answer8', 'answer9',
                  'answer10']
        labels = {
            'answer1': ('Marital Status(Single | Married):'),
            'answer2': ('Family Structure(Nuclear | Joint):'),
            'answer3': ('Have all household members agreed to the adoption?:'),
            'answer4': ('Do you have access to a garden? :'),
            'answer5': ('Is there any animal Shelter near you?:'),
            'answer6': ('No. of Household Members:'),
            'answer7': ('Do you live in a(House/Flat/Apartment):'),
            'answer8': ('Where do you intend on keeping the animal?(Inside House/Outside House):'),
            'answer9': ('Employment status:(Employed | Self-employed | Unemployed | Housewife)'),
            'answer10': ('Do you currently own a pet?(Yes | No):')
        }
