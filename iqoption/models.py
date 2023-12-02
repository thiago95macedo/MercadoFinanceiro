from django.db import models
from datetime import datetime
from django.utils import timezone

class AtivosBinarios(models.Model):

    ativo_binario = models.CharField(verbose_name= 'Ativos Binários', max_length=20)
    ativo_binario_datetime = models.DateTimeField(verbose_name= 'Atualização', auto_now=True)
    ativo_binario_aberto = models.BooleanField(verbose_name= 'Aberto', default=False)
    ativo_binario_m1 = models.BooleanField(verbose_name= 'M1', default=False)
    ativo_binario_m1_lucro = models.DecimalField(verbose_name= 'Lucro M1', max_digits=10, decimal_places=2, default=0.00)
    ativo_binario_m1_lucro_display = models.CharField(verbose_name= 'Lucro M1 Display', max_length=20, default='0%')
    ativo_binario_m5 = models.BooleanField(verbose_name= 'M5', default=False)
    ativo_binario_m5_lucro = models.DecimalField(verbose_name= 'Lucro M5', max_digits=10, decimal_places=2, default=0.00)
    ativo_binario_m5_lucro_display = models.CharField(verbose_name= 'Lucro M5 Display', max_length=20, default='0%')

    def save(self, *args, **kwargs):
        self.ativo_binario_m1_lucro_display = f'{round(self.ativo_binario_m1_lucro * 100, 2)}%'.replace('.', ',')
        self.ativo_binario_m5_lucro_display = f'{round(self.ativo_binario_m5_lucro * 100, 2)}%'.replace('.', ',')
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDCAD
class CandlesAUDCAD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDCAD-OTC
class CandlesAUDCADotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDCHF
class CandlesAUDCHF(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDJPY
class CandlesAUDJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDNZD
class CandlesAUDNZD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo AUDUSD
class CandlesAUDUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo BTCUSD
class CandlesBTCUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo CADCHF
class CandlesCADCHF(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo CADJPY
class CandlesCADJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo CHFJPY
class CandlesCHFJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EOSUSD
class CandlesEOSUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo ETHUSD
class CandlesETHUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURAUD
class CandlesEURAUD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURCAD
class CandlesEURCAD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURCHF
class CandlesEURCHF(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURGBP
class CandlesEURGBP(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURGBP-OTC
class CandlesEURGBPotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURJPY
class CandlesEURJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURJPY-OTC
class CandlesEURJPYotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURNZD
class CandlesEURNZD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURUSD
class CandlesEURUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo EURUSD-OTC
class CandlesEURUSDotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPAUD
class CandlesGBPAUD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPCAD
class CandlesGBPCAD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPCHF
class CandlesGBPCHF(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPJPY
class CandlesGBPJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPJPY-OTC
class CandlesGBPJPYotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPNZD
class CandlesGBPNZD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPUSD
class CandlesGBPUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo GBPUSD-OTC
class CandlesGBPUSDotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo LTCUSD
class CandlesLTCUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo NZDUSD
class CandlesNZDUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo NZDUSD-OTC
class CandlesNZDUSDotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDBRL
class CandlesUSDBRL(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDCAD
class CandlesUSDCAD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDCHF
class CandlesUSDCHF(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDCHF-OTC
class CandlesUSDCHFotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDHKD
class CandlesUSDHKD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDHKD-OTC
class CandlesUSDHKDotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDINR
class CandlesUSDINR(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDINR-OTC
class CandlesUSDINRotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDJPY
class CandlesUSDJPY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDJPY-OTC
class CandlesUSDJPYotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDNOK
class CandlesUSDNOK(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDPLN
class CandlesUSDPLN(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDRUB
class CandlesUSDRUB(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDSEK
class CandlesUSDSEK(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDSGD
class CandlesUSDSGD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDSGD-OTC
class CandlesUSDSGDotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDTRY
class CandlesUSDTRY(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDZAR
class CandlesUSDZAR(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USDZAR-OTC
class CandlesUSDZARotc(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo USOUSD
class CandlesUSOUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo XAUUSD
class CandlesXAUUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)

# Modelo de Dados para Armazenar Informações de Velas do Ativo XRPUSD
class CandlesXRPUSD(models.Model):

    ativo_binario = models.ForeignKey(AtivosBinarios, on_delete=models.CASCADE, verbose_name= 'Ativo Binário', null=True)
    candle_timestamp = models.IntegerField(verbose_name= 'Timestamp', null=True)
    candle_datetime = models.DateTimeField(verbose_name= 'Data e Hora', null=True)
    candle_open = models.DecimalField(verbose_name= 'Abertura', max_digits=10, decimal_places=5, default=0.00)
    candle_high = models.DecimalField(verbose_name= 'Máxima', max_digits=10, decimal_places=5, default=0.00)
    candle_low = models.DecimalField(verbose_name= 'Mínima', max_digits=10, decimal_places=5, default=0.00)
    candle_close = models.DecimalField(verbose_name= 'Fechamento', max_digits=10, decimal_places=5, default=0.00)
    candle_volume = models.DecimalField(verbose_name= 'Volume', max_digits=10, decimal_places=5, default=0.00)

    def __str__(self):
        return f'{self.candle_datetime} - {self.ativo_binario.ativo_binario} - {self.candle_open} - {self.candle_high} - {self.candle_low} - {self.candle_close} - {self.candle_volume}'

    def save(self, *args, **kwargs):
        naive_datetime = datetime.fromtimestamp(self.candle_timestamp)
        aware_datetime = timezone.make_aware(naive_datetime)
        self.candle_datetime = aware_datetime
        super().save(*args, **kwargs)