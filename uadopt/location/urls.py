from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculate_distance_view, name='calculate-view'),

]
api_key = 'AIzaSyBRLOwsUtCMaraWXvjzPAV-WE4M2FRqfUo'