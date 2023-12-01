import logging
from .tasks import login_iqoption, atualizar_ativos_binarios
from accounts.models import IQOption

logger = logging.getLogger(__name__)

def cron_atualizar_ativos_binarios():
    logger.info('Atualizando Ativos Binários')
    iqoption_record_pass = IQOption.objects.get(id=1)  # Substitua 1 pelo ID do seu iqoption_record
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_ativos_binarios(iqoption_record_pass, IQAPI)
    logger.info('Atualização dos Ativos Binários concluída com sucesso!')