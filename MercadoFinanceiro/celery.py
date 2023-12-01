import os
from celery import Celery

# Definindo a variável de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MercadoFinanceiro.settings')

app = Celery('MercadoFinanceiro')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()