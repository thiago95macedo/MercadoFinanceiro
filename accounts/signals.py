from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IQOption
from iqoption.iqoption_metodos import login_iqoption

# Define um sinal Django que é acionado após a gravação (save) de uma instância do modelo IQOption.
# Se o campo 'iqoption_permitir' da instância for verdadeiro, a função 'login_iqoption' é chamada com a instância como argumento.
# @receiver(post_save, sender=IQOption)
# def trigger_login(sender, instance, **kwargs):
#     if instance.iqoption_permitir:
#         login_iqoption(instance)