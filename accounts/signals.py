from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IQOption
from iqoption.iqoption_login import login_iqoption

@receiver(post_save, sender=IQOption)
def trigger_login(sender, instance, **kwargs):
    if instance.iqoption_permitir:
        login_iqoption(instance)