from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class IQOption(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iqoption_permitir = models.BooleanField(verbose_name=' Permitir Operações Trader', default=False)
    iqoption_email = models.CharField(verbose_name='E-mail', max_length=100, blank=True)
    iqoption_password = models.CharField(verbose_name='Senha', max_length=100, blank=True)

    def __str__(self):
        return ''  # retorna uma string vazia
    
    def __unicode__(self):
        return ''  # retorna uma string vazia

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    IQOption.objects.get_or_create(user=instance)
    instance.iqoption.save()