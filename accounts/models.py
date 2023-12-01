from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Definição do modelo IQOption
class IQOption(models.Model):
    # Constantes para os tipos de conta
    REAL = 'REAL'
    PRACTICE = 'PRACTICE'

    # Opções para o campo de escolha do tipo de conta
    TYPE_CHOICES = [
        (REAL, 'Real'),
        (PRACTICE, 'Treinamento'),
    ]

    # Campos do modelo
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iqoption_permitir = models.BooleanField(verbose_name=' Permitir Operações Trader', default=False)
    iqoption_email = models.CharField(verbose_name='E-mail', max_length=100, blank=True)
    iqoption_password = models.CharField(verbose_name='Senha', max_length=100, blank=True)
    iqoption_type = models.CharField(verbose_name='Tipo de Conta', max_length=10, choices=TYPE_CHOICES, default=PRACTICE)
    iqoption_real_saldo = models.DecimalField(verbose_name='Saldo Conta Real', max_digits=10, decimal_places=2, default=0)
    iqoption_real_saldo_display = models.CharField(verbose_name='Saldo Conta Real', max_length=20, default='0,00')
    iqoption_practice_saldo = models.DecimalField(verbose_name='Saldo Conta Treinamento', max_digits=10, decimal_places=2, default=0)
    iqoption_practice_saldo_display = models.CharField(verbose_name='Saldo Conta Treinamento', max_length=20, default='0,00')

    # Método para representação em string do objeto
    def __str__(self):
        return ''  # retorna uma string vazia
    
    # Método para representação unicode do objeto
    def __unicode__(self):
        return ''  # retorna uma string vazia

# Sinal que é disparado após um objeto User ser salvo para atuaçozação do Saldo das Contas Real e Treinamento
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    IQOption.objects.get_or_create(user=instance)
    instance.iqoption.save()

