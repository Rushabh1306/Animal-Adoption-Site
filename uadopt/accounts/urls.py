from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    # path('login', views.loginPage, name='login'),
    path('registration', views.registerPage, name='registration'),
    # path('adminLogin', views.adminLogin, name='adminLogin'),
    # path('adminRegistration', views.adminRegistration, name='adminRegistration'),
    # path('adminIndex',views.adminIndex, name='adminIndex'),
    path('logout', views.logoutUser, name='logout'),
    path('accountInfo', views.accountInfo, name='accountInfo'),
]
