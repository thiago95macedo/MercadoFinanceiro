import logging
from celery import shared_task
from iqoptionapi.stable_api import IQ_Option
from accounts.models import IQOption
from iqoption.models import AtivosBinarios
from decimal import Decimal


# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def login_iqoption(self, iqoption_record_pass):
    IQAPI = IQ_Option(iqoption_record_pass.iqoption_email, iqoption_record_pass.iqoption_password)

    # Definir o cabeçalho e o cookie da sessão
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    cookie = {"Iq": "GOOD"}
    IQAPI.set_session(header, cookie)

    while True:
        if IQAPI.connect():
            logger.info('Conectado com sucesso à IQ Option como %s', iqoption_record_pass.iqoption_email)
            return IQAPI
        else:
            logger.error('Falha ao conectar à IQ Option como %s', iqoption_record_pass.iqoption_email)
            continue

@shared_task(bind=True)
def atualizar_saldo_real(self, iqoption_record, IQAPI):
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return
    # Obter saldo da conta real
    IQAPI.change_balance('REAL')
    real_balance = IQAPI.get_balance()

    # Atualizar o saldo no registro
    iqoption_record.iqoption_real_saldo = real_balance

    # Formatar o saldo e armazená-lo no novo campo
    formatted_real_balance = "{:,.2f}".format(real_balance).replace(",", "x").replace(".", ",").replace("x", ".")
    iqoption_record.iqoption_real_saldo_display = formatted_real_balance
    iqoption_record.save()

    logger.info("Saldo da conta Real atualizado com sucesso!")

@shared_task(bind=True)
def atualizar_saldo_pratica(self, iqoption_record, IQAPI):
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return
        
    # Obter saldo da conta demo (prática)
    IQAPI.change_balance('PRACTICE')
    practice_balance = IQAPI.get_balance()

    # Atualizar o saldo no registro
    iqoption_record.iqoption_practice_saldo = practice_balance

    # Formatar o saldo e armazená-lo no novo campo
    formatted_practice_balance = "{:,.2f}".format(practice_balance).replace(",", "x").replace(".", ",").replace("x", ".")
    iqoption_record.iqoption_practice_saldo_display = formatted_practice_balance
    iqoption_record.save()

    logger.info("Saldo da conta de Treinamento atualizado com sucesso!")

@shared_task(bind=True)
def atualizar_ativos_binarios(self, iqoption_record, IQAPI):
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return
    
    ALL_Asset = IQAPI.get_all_open_time()
    ALL_Profit = IQAPI.get_all_profit()  # Obter informações de lucro

    for ativo in ALL_Asset["turbo"]:
        iqoption_record, created = AtivosBinarios.objects.get_or_create(ativo_binario=ativo)
        iqoption_record.ativo_binario_m1 = ALL_Asset["turbo"][ativo]["open"]
        iqoption_record.ativo_binario_aberto = iqoption_record.ativo_binario_m1
        if ativo in ALL_Profit:
            iqoption_record.ativo_binario_m1_lucro = Decimal(ALL_Profit[ativo]["turbo"])
        if not created:
            # Atualize outros campos do objeto existente aqui
            pass
        iqoption_record.save()

    for ativo in ALL_Asset["binary"]:
        iqoption_record, created = AtivosBinarios.objects.get_or_create(ativo_binario=ativo)
        iqoption_record.ativo_binario_m5 = ALL_Asset["binary"][ativo]["open"]
        iqoption_record.ativo_binario_aberto = iqoption_record.ativo_binario_m5
        if ativo in ALL_Profit:
            iqoption_record.ativo_binario_m5_lucro = Decimal(ALL_Profit[ativo]["binary"])
        if not created:
            # Atualize outros campos do objeto existente aqui
            pass
        iqoption_record.save()

    logger.info('Atualização do status dos ativos concluída.')