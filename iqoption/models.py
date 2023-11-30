from django.db import models

class AtivosBinarios(models.Model):
    ATIVO_CHOICES = [
        ('AUDCAD', 'AUD/CAD'),
        ('AUDJPY', 'AUD/JPY'),
        ('AUDUSD', 'AUD/USD'),
        ('CADCHF', 'CAD/CHF'),
        ('EURGBP', 'EUR/GBP'),
        ('EURJPY', 'EUR/JPY'),
        ('EURUSD', 'EUR/USD'),
        ('GBPJPY', 'GBP/JPY'),
        ('GBPUSD', 'GBP/USD'),
        ('USDJPY', 'USD/JPY'),
        ('USDCAD', 'USD/CAD'),
        ('USDCHF', 'USD/CHF'),
        ('XAUUSD', 'OURO'),
        ('AUDCAD-OTC', 'AUD/CAD (OTC)'),
        ('EURGBP-OTC', 'EUR/GBP (OTC)'),
        ('EURJPY-OTC', 'EUR/JPY (OTC)'),
        ('EURUSD-OTC', 'EUR/USD (OTC)'),
        ('GBPJPY-OTC', 'GBP/JPY (OTC)'),
        ('GBPUSD-OTC', 'GBP/USD (OTC)'),
        ('NZDUSD-OTC', 'NZD/USD (OTC)'),
        ('USDCHF-OTC', 'USD/CHF (OTC)'),
        ('USDJPY-OTC', 'USD/JPY (OTC)'),
    ]

    ativo_binario = models.CharField(verbose_name= 'Ativi Binário', max_length=20, choices=ATIVO_CHOICES)
    ativo_binario_aberto = models.BooleanField(verbose_name= 'Aberto', default=False)
    ativo_binario_m1 = models.BooleanField(verbose_name= 'M1', default=False)
    ativo_binario_m1_lucro = models.DecimalField(verbose_name= 'Lucro M1', max_digits=10, decimal_places=2)
    ativo_binario_m5 = models.BooleanField(verbose_name= 'M5', default=False)
    ativo_binario_m5_lucro = models.DecimalField(verbose_name= 'Lucro M5', max_digits=10, decimal_places=2)
