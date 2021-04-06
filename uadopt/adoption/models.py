from django.db import models


# Create your models here.


class Animal(models.Model):
    owner_id = models.IntegerField()
    p_animalpic = models.ImageField(upload_to='animalpic', default='animalpic/default.jpg')
    p_name = models.CharField(max_length=12)
    p_type = models.CharField(max_length=20)
    p_breed = models.CharField(max_length=20)
    p_age = models.IntegerField()
    p_location = models.CharField(max_length=50, default='None')
    p_gender = models.CharField(max_length=7)
    p_vaccination = models.CharField(max_length=4)
    p_desc = models.TextField()


maritial_status = \
    [
        ('single', 'Single'),
        ('married', 'married'),
    ]


class Evaluation(models.Model):
    user_id = models.IntegerField(null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True)
    answer1 = models.CharField(max_length=14, blank=True)
    answer2 = models.CharField(max_length=14, blank=True)
    answer3 = models.CharField(max_length=14, blank=True)
    answer4 = models.CharField(max_length=14, blank=True)
    answer5 = models.CharField(max_length=14, blank=True)
    answer6 = models.CharField(max_length=14, blank=True)
    answer7 = models.CharField(max_length=14, blank=True)
    answer8 = models.CharField(max_length=14, blank=True)
    answer9 = models.CharField(max_length=14, blank=True)
    answer10 = models.CharField(max_length=14, blank=True)


class Request(models.Model):
    user_id = models.IntegerField()
    admin_id = models.IntegerField()
    animal_id = models.IntegerField()
    type = models.CharField(max_length=10, null=True)
    pickup_id = models.IntegerField(default=-1)
    status = models.CharField(max_length=10, default='pending')  # granted,rejected and pending
