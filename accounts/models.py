from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, blank=True)
    mobile = models.CharField(max_length=11, blank=True)
    iqoption = models.BooleanField(default=False)
    iqoption_email = models.CharField(max_length=100, blank=True)
    iqoption_password = models.CharField(max_length=100, blank=True)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()