from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adoption/adopt_a_pet', views.adopt_a_pet, name='adopt_a_pet'),
    path('adoption/animalInfo/<int:animalId>', views.animalInfo, name='animalInfo'),
    path('adoption/evaluation/<int:animalId>', views.evaluation, name='evaluation'),
    path('adoption/overview/<str:animalId>', views.overview, name='overview'),
    path('adoption/requestSend/<int:animalId>', views.requestSend, name='requestSend'),
    path('adoption/thankyou', views.thankYou, name='thankyou'),
    path('adoption/aboutus', views.aboutUs, name='aboutus'),
    path('adoption/support', views.support, name='support'),
    path('adoption/notification', views.notificationList, name='notification'),
    path('adoption/conversation', views.conversationList, name='conversation'),
    path('adoption/notification/<int:reqid>', views.notification, name='notification'),
    path('adoption/conversation/<int:cid>', views.conversation, name='conversation'),

]
