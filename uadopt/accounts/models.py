from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db import models

# Create your models here.


from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class userDetails(models.Model):
    user_id = models.IntegerField()
    address = models.TextField(blank=True)
    city = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zipcode = models.CharField(max_length=6, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
