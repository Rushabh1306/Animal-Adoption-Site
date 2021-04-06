from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm

from .models import AdminPanel
from adoption.models import Animal


class CreateAdminUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CreateOrgForm(ModelForm):
    class Meta:
        model = AdminPanel
        fields = ['org_name', 'org_phone', 'org_address', 'org_city', 'org_state', 'org_zipcode', 'org_doc']


class OrgForm(ModelForm):
    class Meta:
        model = AdminPanel
        fields = ['org_name', 'org_address', 'org_city', 'org_state']


class CreatePetForm(ModelForm):
    # owner_id = forms.IntegerField(disabled=True)

    class Meta:
        model = Animal
        fields = '__all__'
        exclude = ('owner_id',)
        # readonly_fields = ('owner_id',)
