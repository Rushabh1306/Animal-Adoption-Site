from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class AdminPanel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def isadmin(self):
        if self.is_admin:
            return True
        return False


