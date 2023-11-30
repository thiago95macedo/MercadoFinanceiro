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

    ativo_binario = models.CharField(max_length=20, choices=ATIVO_CHOICES)
    ativo_binario_aberto = models.BooleanField(default=False)
    ativo_binario_m1 = models.DecimalField(max_digits=10, decimal_places=2)
    ativo_binario_m1_lucro = models.DecimalField(max_digits=10, decimal_places=2)
    ativo_binario_m5 = models.DecimalField(max_digits=10, decimal_places=2)
    ativo_binario_m5_lucro = models.DecimalField(max_digits=10, decimal_places=2)
