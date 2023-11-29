# Generated by Django 4.2.7 on 2023-11-29 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(blank=True, max_length=11)),
                ('mobile', models.CharField(blank=True, max_length=11)),
                ('iqoption', models.BooleanField(default=False)),
                ('iqoption_email', models.CharField(blank=True, max_length=100)),
                ('iqoption_password', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]