import logging
from iqoptionapi.stable_api import IQ_Option
from accounts.models import IQOption

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_iqoption(iqoption_record):
    IQAPI = IQ_Option(iqoption_record.iqoption_email, iqoption_record.iqoption_password)
    if IQAPI.connect():
        logger.info('Conectado com sucesso à IQ Option como %s', iqoption_record.iqoption_email)
        return IQAPI
    else:
        logger.error('Falha ao conectar à IQ Option como %s', iqoption_record.iqoption_email)
        return None

def test_login():
    # Obter o primeiro registro do modelo IQOption
    iqoption_record = IQOption.objects.first()
    if not iqoption_record:
        logger.error('Nenhum registro encontrado no modelo IQOption')
        return

    # Tentar se conectar à IQ Option
    IQAPI = login_iqoption(iqoption_record)

test_login()