# Generated by Django 4.2.7 on 2023-12-01 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iqoption', '0007_ativosbinarios_ativo_binario_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandlesEURUSD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candle_timestamp', models.IntegerField(null=True, verbose_name='Timestamp')),
                ('candle_datetime', models.DateTimeField(null=True, verbose_name='Data e Hora')),
                ('candle_open', models.DecimalField(decimal_places=5, default=0.0, max_digits=10, verbose_name='Abertura')),
                ('candle_high', models.DecimalField(decimal_places=5, default=0.0, max_digits=10, verbose_name='Máxima')),
                ('candle_low', models.DecimalField(decimal_places=5, default=0.0, max_digits=10, verbose_name='Mínima')),
                ('candle_close', models.DecimalField(decimal_places=5, default=0.0, max_digits=10, verbose_name='Fechamento')),
                ('candle_volume', models.DecimalField(decimal_places=5, default=0.0, max_digits=10, verbose_name='Volume')),
                ('ativo_binario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='iqoption.ativosbinarios', verbose_name='Ativo Binário')),
            ],
        ),
    ]
