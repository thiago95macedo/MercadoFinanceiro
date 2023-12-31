# Generated by Django 4.2.7 on 2023-12-01 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iqoption', '0002_alter_ativosbinarios_ativo_binario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario',
            field=models.CharField(max_length=20, verbose_name='Ativos Binários'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_aberto',
            field=models.BooleanField(default=False, verbose_name='Aberto'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m1',
            field=models.BooleanField(default=False, verbose_name='M1'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m1_lucro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Lucro M1'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m5',
            field=models.BooleanField(default=False, verbose_name='M5'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m5_lucro',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Lucro M5'),
        ),
    ]
