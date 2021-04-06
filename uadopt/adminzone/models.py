from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save


class AdminPanel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(default=False)
    org_name = models.CharField(max_length=50, null=True)
    org_phone = models.CharField(max_length=12, null=True)
    org_address = models.TextField(null=True)
    org_city = models.CharField(max_length=20, null=True)
    org_state = models.CharField(max_length=15, null=True)
    org_zipcode = models.CharField(max_length=6, null=True)
    org_location = models.CharField(max_length=20, null=True)
    org_doc = models.FileField(upload_to='admindocs', default='admindocs/default.jpg')

    def isadmin(self):
        if self.is_admin:
            return True
        return False


def create_admin_panel(sender, instance, created, **kwargs):
    if created:
        AdminPanel.objects.create(user=instance)


post_save.connect(create_admin_panel, sender=User)
