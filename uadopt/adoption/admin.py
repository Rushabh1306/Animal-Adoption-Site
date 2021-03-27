from django.contrib import admin
from .models import Animal,Evaluation,Request
# Register your models here.
admin.site.register(Animal)
admin.site.register(Evaluation)
admin.site.register(Request)