from django.db import models

class AtivosBinarios(models.Model):

    ativo_binario = models.CharField(verbose_name= 'Ativos Binários', max_length=20)
    ativo_binario_aberto = models.BooleanField(verbose_name= 'Aberto', default=False)
    ativo_binario_m1 = models.BooleanField(verbose_name= 'M1', default=False)
    ativo_binario_m1_lucro = models.DecimalField(verbose_name= 'Lucro M1', max_digits=10, decimal_places=2)
    ativo_binario_m5 = models.BooleanField(verbose_name= 'M5', default=False)
    ativo_binario_m5_lucro = models.DecimalField(verbose_name= 'Lucro M5', max_digits=10, decimal_places=2)
