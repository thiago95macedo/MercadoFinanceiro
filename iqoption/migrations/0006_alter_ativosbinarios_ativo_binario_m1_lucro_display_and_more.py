# Generated by Django 4.2.7 on 2023-12-01 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iqoption', '0005_alter_ativosbinarios_ativo_binario_m1_lucro_display_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m1_lucro_display',
            field=models.CharField(default='0%', max_length=20, verbose_name='Lucro M1 Display'),
        ),
        migrations.AlterField(
            model_name='ativosbinarios',
            name='ativo_binario_m5_lucro_display',
            field=models.CharField(default='0%', max_length=20, verbose_name='Lucro M5 Display'),
        ),
    ]
