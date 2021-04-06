from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.adminIndex, name='adminIndex'),
    path('login', views.adminLogin, name='adminLogin'),
    # path('login', views.adminLogin, name='adminLogin'),
    path('registration', views.adminRegister, name='adminRegistration'),
    path('logout', views.adminLogoutUser, name='adminLogout'),
    path('accountInfo', views.accountInfo, name='accountInfo'),
    #
    path('viewRequest', views.viewRequest, name='viewRequest'),
    path('viewRequestInfo/<int:reqid>', views.viewRequestInfo, name='viewRequestInfo'),
    path('confirmRequest/<int:reqid>', views.confirmRequest, name='confirmRequest'),
    path('rejectedRequest/<int:reqid>', views.rejectedRequest, name='rejectedRequest'),

    path('pets', views.pets, name='pets'),
    path('pets/modify/<int:animalId>', views.modifyPets, name='modifyPets'),
    path('pets/add-pet', views.addPets, name='addPets'),
    path('pets/delete/<int:animalId>', views.deletePets, name='delete'),

    path('viewQuestions', views.viewQuestions, name='viewQuestions')

    # path('adoption/overview/<int:animalId>', views.overview, name='overview'),
    # path('adoption/requestSend/<int:animalId>', views.requestSend, name='requestSend'),
    # path('adoption/thankyou', views.thankYou, name='thankyou'),
]
