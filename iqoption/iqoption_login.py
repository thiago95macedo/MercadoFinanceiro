import logging
from iqoptionapi.stable_api import IQ_Option
from accounts.models import IQOption

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_iqoption(iqoption_record):
    IQAPI = IQ_Option(iqoption_record.iqoption_email, iqoption_record.iqoption_password)

    # Definir o cabeçalho e o cookie da sessão
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    cookie = {"Iq": "GOOD"}
    IQAPI.set_session(header, cookie)

    while True:
        if IQAPI.connect():
            logger.info('Conectado com sucesso à IQ Option como %s', iqoption_record.iqoption_email)
            return IQAPI
        else:
            logger.error('Falha ao conectar à IQ Option como %s', iqoption_record.iqoption_email)
            continue