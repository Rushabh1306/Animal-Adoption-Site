from django.db import models


# Create your models here.


class Animal(models.Model):
    owner_id = models.IntegerField()
    p_animalpic = models.ImageField(upload_to='animalpic',default='animalpic/default.jpg')
    p_name = models.CharField(max_length=12)
    p_type = models.CharField(max_length=20)
    p_breed = models.CharField(max_length=20)
    p_age = models.IntegerField()
    p_location = models.CharField(max_length=50,default='None')
    p_gender = models.CharField(max_length=7)
    p_vaccination = models.CharField(max_length=4)
    p_desc = models.TextField()


class Evaluation(models.Model):
    user_id = models.IntegerField()
    animal=models.ForeignKey(Animal,on_delete=models.CASCADE,null=True)
    evaluation_details = models.TextField()


class Request(models.Model):
    user_id = models.IntegerField()
    admin_id = models.IntegerField()
    animal_id = models.IntegerField()
    type = models.CharField(max_length=10,null=True)
    pickup_id = models.IntegerField(default=-1)
    status = models.CharField(max_length=10,default='pending')  # Approved,Declined and Pending


class notifications(models.Model):
    pass