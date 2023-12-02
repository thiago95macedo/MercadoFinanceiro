from celery import shared_task
from iqoptionapi.stable_api import IQ_Option
from iqoption.models import AtivosBinarios
from iqoption.models import CandlesAUDCAD, CandlesAUDCADotc, CandlesAUDCHF, CandlesAUDJPY, CandlesAUDNZD 
from iqoption.models import CandlesAUDUSD, CandlesBTCUSD, CandlesCADCHF, CandlesCADJPY, CandlesCHFJPY
from iqoption.models import CandlesEOSUSD, CandlesETHUSD, CandlesEURAUD, CandlesEURCAD, CandlesEURCHF
from iqoption.models import CandlesEURGBP, CandlesEURGBPotc, CandlesEURJPY, CandlesEURJPYotc, CandlesEURNZD
from iqoption.models import CandlesEURUSD, CandlesEURUSDotc, CandlesGBPAUD, CandlesGBPCAD, CandlesGBPCHF
from iqoption.models import CandlesGBPJPY, CandlesGBPJPYotc, CandlesGBPNZD, CandlesGBPUSD, CandlesGBPUSDotc
from iqoption.models import CandlesLTCUSD, CandlesNZDUSD, CandlesNZDUSDotc, CandlesUSDBRL, CandlesUSDCAD
from iqoption.models import CandlesUSDCHF, CandlesUSDCHFotc, CandlesUSDHKD, CandlesUSDHKDotc, CandlesUSDINR
from iqoption.models import CandlesUSDINRotc, CandlesUSDJPY, CandlesUSDJPYotc, CandlesUSDNOK, CandlesUSDPLN
from iqoption.models import CandlesUSDRUB, CandlesUSDSEK, CandlesUSDSGD, CandlesUSDSGDotc, CandlesUSDTRY
from iqoption.models import CandlesUSDZAR, CandlesUSDZARotc, CandlesUSOUSD, CandlesXAUUSD, CandlesXRPUSD
from decimal import Decimal
import logging


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

# AUDCAD - Atuaçização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audcad(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audcad.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDCAD
    audcad = AtivosBinarios.objects.get(ativo_binario='AUDCAD')

    logger.info('Ativo binário AUDCAD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDCAD', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDCAD.')

    # Verifique se o ativo binário está aberto
    if not audcad.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDCAD', 60)
        logger.info('Ativo binário AUDCAD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDCAD
    candles = IQAPI.get_realtime_candles('AUDCAD', 60)

    logger.info('Informações das velas obtidas para AUDCAD.')

    # Crie um novo objeto CandlesAUDCAD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDCAD(
            ativo_binario=audcad,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDCADotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audcad concluída.')

# AUDCAD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audcadotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audcadotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDCAD-OTC
    audcad_otc = AtivosBinarios.objects.get(ativo_binario='AUDCAD-OTC')

    logger.info('Ativo binário AUDCAD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDCAD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDCAD-OTC.')

    # Verifique se o ativo binário está aberto
    if not audcad_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDCAD-OTC', 60)
        logger.info('Ativo binário AUDCAD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDCAD-OTC
    candles = IQAPI.get_realtime_candles('AUDCAD-OTC', 60)

    logger.info('Informações das velas obtidas para AUDCAD-OTC.')

    # Crie um novo objeto CandlesAUDCAD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDCADotc(
            ativo_binario=audcad_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDCADotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audcadotc concluída.')

# AUDCHF - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audchf(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audchf.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDCHF
    audchf = AtivosBinarios.objects.get(ativo_binario='AUDCHF')

    logger.info('Ativo binário AUDCHF obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDCHF', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDCHF.')

    # Verifique se o ativo binário está aberto
    if not audchf.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDCHF', 60)
        logger.info('Ativo binário AUDCHF não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDCHF
    candles = IQAPI.get_realtime_candles('AUDCHF', 60)

    logger.info('Informações das velas obtidas para AUDCHF.')

    # Crie um novo objeto CandlesAUDCHF para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDCHF(
            ativo_binario=audchf,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDCHF salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audchf concluída.')


# AUDJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDJPY
    audjpy = AtivosBinarios.objects.get(ativo_binario='AUDJPY')

    logger.info('Ativo binário AUDJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDJPY.')

    # Verifique se o ativo binário está aberto
    if not audjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDJPY', 60)
        logger.info('Ativo binário AUDJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDJPY
    candles = IQAPI.get_realtime_candles('AUDJPY', 60)

    logger.info('Informações das velas obtidas para AUDJPY.')

    # Crie um novo objeto CandlesAUDJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDJPY(
            ativo_binario=audjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audjpy concluída.')

# AUDNZD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audnzd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audnzd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDNZD
    audnzd = AtivosBinarios.objects.get(ativo_binario='AUDNZD')

    logger.info('Ativo binário AUDNZD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDNZD', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDNZD.')

    # Verifique se o ativo binário está aberto
    if not audnzd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDNZD', 60)
        logger.info('Ativo binário AUDNZD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDNZD
    candles = IQAPI.get_realtime_candles('AUDNZD', 60)

    logger.info('Informações das velas obtidas para AUDNZD.')

    # Crie um novo objeto CandlesAUDNZD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDNZD(
            ativo_binario=audnzd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDNZD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audnzd concluída.')


# AUDUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_audusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_audusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para AUDUSD
    audusd = AtivosBinarios.objects.get(ativo_binario='AUDUSD')

    logger.info('Ativo binário AUDUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('AUDUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para AUDUSD.')

    # Verifique se o ativo binário está aberto
    if not audusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('AUDUSD', 60)
        logger.info('Ativo binário AUDUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o AUDUSD
    candles = IQAPI.get_realtime_candles('AUDUSD', 60)

    logger.info('Informações das velas obtidas para AUDUSD.')

    # Crie um novo objeto CandlesAUDUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesAUDUSD(
            ativo_binario=audusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesAUDUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_audusd concluída.')

# BTCUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_btcusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_btcusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para BTCUSD
    btcusd = AtivosBinarios.objects.get(ativo_binario='BTCUSD')

    logger.info('Ativo binário BTCUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('BTCUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para BTCUSD.')

    # Verifique se o ativo binário está aberto
    if not btcusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('BTCUSD', 60)
        logger.info('Ativo binário BTCUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o BTCUSD
    candles = IQAPI.get_realtime_candles('BTCUSD', 60)

    logger.info('Informações das velas obtidas para BTCUSD.')

    # Crie um novo objeto CandlesBTCUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesBTCUSD(
            ativo_binario=btcusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesBTCUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_btcusd concluída.')

# CADCHF - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_cadchf(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_cadchf.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para CADCHF
    cadchf = AtivosBinarios.objects.get(ativo_binario='CADCHF')

    logger.info('Ativo binário CADCHF obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('CADCHF', 60, 1)

    logger.info('Fluxo de velas iniciado para CADCHF.')

    # Verifique se o ativo binário está aberto
    if not cadchf.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('CADCHF', 60)
        logger.info('Ativo binário CADCHF não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o CADCHF
    candles = IQAPI.get_realtime_candles('CADCHF', 60)

    logger.info('Informações das velas obtidas para CADCHF.')

    # Crie um novo objeto CandlesCADCHF para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesCADCHF(
            ativo_binario=cadchf,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesCADCHF salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_cadchf concluída.')

# CADJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_cadjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_cadjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para CADJPY
    cadjpy = AtivosBinarios.objects.get(ativo_binario='CADJPY')

    logger.info('Ativo binário CADJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('CADJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para CADJPY.')

    # Verifique se o ativo binário está aberto
    if not cadjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('CADJPY', 60)
        logger.info('Ativo binário CADJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o CADJPY
    candles = IQAPI.get_realtime_candles('CADJPY', 60)

    logger.info('Informações das velas obtidas para CADJPY.')

    # Crie um novo objeto CandlesCADJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesCADJPY(
            ativo_binario=cadjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesCADJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_cadjpy concluída.')

# CHFJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_chfjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_chfjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para CHFJPY
    chfjpy = AtivosBinarios.objects.get(ativo_binario='CHFJPY')

    logger.info('Ativo binário CHFJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('CHFJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para CHFJPY.')

    # Verifique se o ativo binário está aberto
    if not chfjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('CHFJPY', 60)
        logger.info('Ativo binário CHFJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o CHFJPY
    candles = IQAPI.get_realtime_candles('CHFJPY', 60)

    logger.info('Informações das velas obtidas para CHFJPY.')

    # Crie um novo objeto CandlesCHFJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesCHFJPY(
            ativo_binario=chfjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesCHFJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_chfjpy concluída.')

# EOSUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eosusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eosusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EOSUSD
    eosusd = AtivosBinarios.objects.get(ativo_binario='EOSUSD')

    logger.info('Ativo binário EOSUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EOSUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para EOSUSD.')

    # Verifique se o ativo binário está aberto
    if not eosusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EOSUSD', 60)
        logger.info('Ativo binário EOSUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EOSUSD
    candles = IQAPI.get_realtime_candles('EOSUSD', 60)

    logger.info('Informações das velas obtidas para EOSUSD.')

    # Crie um novo objeto CandlesEOSUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEOSUSD(
            ativo_binario=eosusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEOSUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eosusd concluída.')

# ETHUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_ethusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_ethusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para ETHUSD
    ethusd = AtivosBinarios.objects.get(ativo_binario='ETHUSD')

    logger.info('Ativo binário ETHUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('ETHUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para ETHUSD.')

    # Verifique se o ativo binário está aberto
    if not ethusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('ETHUSD', 60)
        logger.info('Ativo binário ETHUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o ETHUSD
    candles = IQAPI.get_realtime_candles('ETHUSD', 60)

    logger.info('Informações das velas obtidas para ETHUSD.')

    # Crie um novo objeto CandlesETHUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesETHUSD(
            ativo_binario=ethusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesETHUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_ethusd concluída.')

# EURAUD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_euraud(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_euraud.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURAUD
    euraud = AtivosBinarios.objects.get(ativo_binario='EURAUD')

    logger.info('Ativo binário EURAUD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURAUD', 60, 1)

    logger.info('Fluxo de velas iniciado para EURAUD.')

    # Verifique se o ativo binário está aberto
    if not euraud.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURAUD', 60)
        logger.info('Ativo binário EURAUD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURAUD
    candles = IQAPI.get_realtime_candles('EURAUD', 60)

    logger.info('Informações das velas obtidas para EURAUD.')

    # Crie um novo objeto CandlesEURAUD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURAUD(
            ativo_binario=euraud,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURAUD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_euraud concluída.')

# EURCAD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurcad(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurcad.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURCAD
    eurcad = AtivosBinarios.objects.get(ativo_binario='EURCAD')

    logger.info('Ativo binário EURCAD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURCAD', 60, 1)

    logger.info('Fluxo de velas iniciado para EURCAD.')

    # Verifique se o ativo binário está aberto
    if not eurcad.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURCAD', 60)
        logger.info('Ativo binário EURCAD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURCAD
    candles = IQAPI.get_realtime_candles('EURCAD', 60)

    logger.info('Informações das velas obtidas para EURCAD.')

    # Crie um novo objeto CandlesEURCAD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURCAD(
            ativo_binario=eurcad,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURCAD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurcad concluída.')

# EURCHF - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurchf(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurchf.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURCHF
    eurchf = AtivosBinarios.objects.get(ativo_binario='EURCHF')

    logger.info('Ativo binário EURCHF obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURCHF', 60, 1)

    logger.info('Fluxo de velas iniciado para EURCHF.')

    # Verifique se o ativo binário está aberto
    if not eurchf.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURCHF', 60)
        logger.info('Ativo binário EURCHF não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURCHF
    candles = IQAPI.get_realtime_candles('EURCHF', 60)

    logger.info('Informações das velas obtidas para EURCHF.')

    # Crie um novo objeto CandlesEURCHF para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURCHF(
            ativo_binario=eurchf,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURCHF salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurchf concluída.')

# EURGBP - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurgbp(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurgbp.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURGBP
    eurgbp = AtivosBinarios.objects.get(ativo_binario='EURGBP')

    logger.info('Ativo binário EURGBP obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURGBP', 60, 1)

    logger.info('Fluxo de velas iniciado para EURGBP.')

    # Verifique se o ativo binário está aberto
    if not eurgbp.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURGBP', 60)
        logger.info('Ativo binário EURGBP não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURGBP
    candles = IQAPI.get_realtime_candles('EURGBP', 60)

    logger.info('Informações das velas obtidas para EURGBP.')

    # Crie um novo objeto CandlesEURGBP para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURGBP(
            ativo_binario=eurgbp,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURGBP salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurgbp concluída.')

# EURGBP-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurgbpotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurgbpotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURGBP-OTC
    eurgbp_otc = AtivosBinarios.objects.get(ativo_binario='EURGBP-OTC')

    logger.info('Ativo binário EURGBP-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURGBP-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para EURGBP-OTC.')

    # Verifique se o ativo binário está aberto
    if not eurgbp_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURGBP-OTC', 60)
        logger.info('Ativo binário EURGBP-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURGBP-OTC
    candles = IQAPI.get_realtime_candles('EURGBP-OTC', 60)

    logger.info('Informações das velas obtidas para EURGBP-OTC.')

    # Crie um novo objeto CandlesEURGBPotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURGBPotc(
            ativo_binario=eurgbp_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURGBPotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurgbpotc concluída.')

# EURJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURJPY
    eurjpy = AtivosBinarios.objects.get(ativo_binario='EURJPY')

    logger.info('Ativo binário EURJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para EURJPY.')

    # Verifique se o ativo binário está aberto
    if not eurjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURJPY', 60)
        logger.info('Ativo binário EURJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURJPY
    candles = IQAPI.get_realtime_candles('EURJPY', 60)

    logger.info('Informações das velas obtidas para EURJPY.')

    # Crie um novo objeto CandlesEURJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURJPY(
            ativo_binario=eurjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurjpy concluída.')

# EURJPY-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurjpyotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurjpyotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURJPY-OTC
    eurjpy_otc = AtivosBinarios.objects.get(ativo_binario='EURJPY-OTC')

    logger.info('Ativo binário EURJPY-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURJPY-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para EURJPY-OTC.')

    # Verifique se o ativo binário está aberto
    if not eurjpy_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURJPY-OTC', 60)
        logger.info('Ativo binário EURJPY-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURJPY-OTC
    candles = IQAPI.get_realtime_candles('EURJPY-OTC', 60)

    logger.info('Informações das velas obtidas para EURJPY-OTC.')

    # Crie um novo objeto CandlesEURJPYotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURJPYotc(
            ativo_binario=eurjpy_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURJPYotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurjpyotc concluída.')

# EURNZD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurnzd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurnzd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURNZD
    eurnzd = AtivosBinarios.objects.get(ativo_binario='EURNZD')

    logger.info('Ativo binário EURNZD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURNZD', 60, 1)

    logger.info('Fluxo de velas iniciado para EURNZD.')

    # Verifique se o ativo binário está aberto
    if not eurnzd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURNZD', 60)
        logger.info('Ativo binário EURNZD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURNZD
    candles = IQAPI.get_realtime_candles('EURNZD', 60)

    logger.info('Informações das velas obtidas para EURNZD.')

    # Crie um novo objeto CandlesEURNZD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURNZD(
            ativo_binario=eurnzd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURNZD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurnzd concluída.')

# EURUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURUSD
    eurusd = AtivosBinarios.objects.get(ativo_binario='EURUSD')

    logger.info('Ativo binário EURUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para EURUSD.')

    # Verifique se o ativo binário está aberto
    if not eurusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURUSD', 60)
        logger.info('Ativo binário EURUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURUSD
    candles = IQAPI.get_realtime_candles('EURUSD', 60)

    logger.info('Informações das velas obtidas para EURUSD.')

    # Crie um novo objeto CandlesEURUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURUSD(
            ativo_binario=eurusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurusd concluída.')

# EURUSD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_eurusdotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_eurusdotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para EURUSD-OTC
    eurusd_otc = AtivosBinarios.objects.get(ativo_binario='EURUSD-OTC')

    logger.info('Ativo binário EURUSD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('EURUSD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para EURUSD-OTC.')

    # Verifique se o ativo binário está aberto
    if not eurusd_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('EURUSD-OTC', 60)
        logger.info('Ativo binário EURUSD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o EURUSD-OTC
    candles = IQAPI.get_realtime_candles('EURUSD-OTC', 60)

    logger.info('Informações das velas obtidas para EURUSD-OTC.')

    # Crie um novo objeto CandlesEURUSDotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesEURUSDotc(
            ativo_binario=eurusd_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesEURUSDotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_eurusdotc concluída.')

# GBPAUD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpaud(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpaud.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPAUD
    gbpaud = AtivosBinarios.objects.get(ativo_binario='GBPAUD')

    logger.info('Ativo binário GBPAUD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPAUD', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPAUD.')

    # Verifique se o ativo binário está aberto
    if not gbpaud.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPAUD', 60)
        logger.info('Ativo binário GBPAUD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPAUD
    candles = IQAPI.get_realtime_candles('GBPAUD', 60)

    logger.info('Informações das velas obtidas para GBPAUD.')

    # Crie um novo objeto CandlesGBPAUD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPAUD(
            ativo_binario=gbpaud,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPAUD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpaud concluída.')

# GBPCAD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpcad(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpcad.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPCAD
    gbpcad = AtivosBinarios.objects.get(ativo_binario='GBPCAD')

    logger.info('Ativo binário GBPCAD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPCAD', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPCAD.')

    # Verifique se o ativo binário está aberto
    if not gbpcad.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPCAD', 60)
        logger.info('Ativo binário GBPCAD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPCAD
    candles = IQAPI.get_realtime_candles('GBPCAD', 60)

    logger.info('Informações das velas obtidas para GBPCAD.')

    # Crie um novo objeto CandlesGBPCAD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPCAD(
            ativo_binario=gbpcad,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPCAD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpcad concluída.')

# GBPCHF - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpchf(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpchf.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPCHF
    gbpchf = AtivosBinarios.objects.get(ativo_binario='GBPCHF')

    logger.info('Ativo binário GBPCHF obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPCHF', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPCHF.')

    # Verifique se o ativo binário está aberto
    if not gbpchf.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPCHF', 60)
        logger.info('Ativo binário GBPCHF não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPCHF
    candles = IQAPI.get_realtime_candles('GBPCHF', 60)

    logger.info('Informações das velas obtidas para GBPCHF.')

    # Crie um novo objeto CandlesGBPCHF para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPCHF(
            ativo_binario=gbpchf,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPCHF salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpchf concluída.')

# GBPJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPJPY
    gbpjpy = AtivosBinarios.objects.get(ativo_binario='GBPJPY')

    logger.info('Ativo binário GBPJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPJPY.')

    # Verifique se o ativo binário está aberto
    if not gbpjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPJPY', 60)
        logger.info('Ativo binário GBPJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPJPY
    candles = IQAPI.get_realtime_candles('GBPJPY', 60)

    logger.info('Informações das velas obtidas para GBPJPY.')

    # Crie um novo objeto CandlesGBPJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPJPY(
            ativo_binario=gbpjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpjpy concluída.')

# GBPJPY-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpjpyotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpjpyotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPJPY-OTC
    gbpjpy_otc = AtivosBinarios.objects.get(ativo_binario='GBPJPY-OTC')

    logger.info('Ativo binário GBPJPY-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPJPY-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPJPY-OTC.')

    # Verifique se o ativo binário está aberto
    if not gbpjpy_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPJPY-OTC', 60)
        logger.info('Ativo binário GBPJPY-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPJPY-OTC
    candles = IQAPI.get_realtime_candles('GBPJPY-OTC', 60)

    logger.info('Informações das velas obtidas para GBPJPY-OTC.')

    # Crie um novo objeto CandlesGBPJPYotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPJPYotc(
            ativo_binario=gbpjpy_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPJPYotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpjpyotc concluída.')

# GBPNZD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpnzd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpnzd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPNZD
    gbpnzd = AtivosBinarios.objects.get(ativo_binario='GBPNZD')

    logger.info('Ativo binário GBPNZD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPNZD', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPNZD.')

    # Verifique se o ativo binário está aberto
    if not gbpnzd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPNZD', 60)
        logger.info('Ativo binário GBPNZD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPNZD
    candles = IQAPI.get_realtime_candles('GBPNZD', 60)

    logger.info('Informações das velas obtidas para GBPNZD.')

    # Crie um novo objeto CandlesGBPNZD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPNZD(
            ativo_binario=gbpnzd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPNZD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpnzd concluída.')

# GBPUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPUSD
    gbpusd = AtivosBinarios.objects.get(ativo_binario='GBPUSD')

    logger.info('Ativo binário GBPUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPUSD.')

    # Verifique se o ativo binário está aberto
    if not gbpusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPUSD', 60)
        logger.info('Ativo binário GBPUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPUSD
    candles = IQAPI.get_realtime_candles('GBPUSD', 60)

    logger.info('Informações das velas obtidas para GBPUSD.')

    # Crie um novo objeto CandlesGBPUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPUSD(
            ativo_binario=gbpusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpusd concluída.')

# GBPUSD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_gbpusdotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_gbpusdotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para GBPUSD-OTC
    gbpusd_otc = AtivosBinarios.objects.get(ativo_binario='GBPUSD-OTC')

    logger.info('Ativo binário GBPUSD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('GBPUSD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para GBPUSD-OTC.')

    # Verifique se o ativo binário está aberto
    if not gbpusd_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('GBPUSD-OTC', 60)
        logger.info('Ativo binário GBPUSD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o GBPUSD-OTC
    candles = IQAPI.get_realtime_candles('GBPUSD-OTC', 60)

    logger.info('Informações das velas obtidas para GBPUSD-OTC.')

    # Crie um novo objeto CandlesGBPUSDotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesGBPUSDotc(
            ativo_binario=gbpusd_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesGBPUSDotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_gbpusdotc concluída.')

# LTCUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_ltcusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_ltcusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para LTCUSD
    ltcusd = AtivosBinarios.objects.get(ativo_binario='LTCUSD')

    logger.info('Ativo binário LTCUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('LTCUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para LTCUSD.')

    # Verifique se o ativo binário está aberto
    if not ltcusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('LTCUSD', 60)
        logger.info('Ativo binário LTCUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o LTCUSD
    candles = IQAPI.get_realtime_candles('LTCUSD', 60)

    logger.info('Informações das velas obtidas para LTCUSD.')

    # Crie um novo objeto CandlesLTCUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesLTCUSD(
            ativo_binario=ltcusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesLTCUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_ltcusd concluída.')

# NZDUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_nzdusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_nzdusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para NZDUSD
    nzdusd = AtivosBinarios.objects.get(ativo_binario='NZDUSD')

    logger.info('Ativo binário NZDUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('NZDUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para NZDUSD.')

    # Verifique se o ativo binário está aberto
    if not nzdusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('NZDUSD', 60)
        logger.info('Ativo binário NZDUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o NZDUSD
    candles = IQAPI.get_realtime_candles('NZDUSD', 60)

    logger.info('Informações das velas obtidas para NZDUSD.')

    # Crie um novo objeto CandlesNZDUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesNZDUSD(
            ativo_binario=nzdusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesNZDUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_nzdusd concluída.')

# NZDUSD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_nzdusdotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_nzdusdotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para NZDUSD-OTC
    nzdusd_otc = AtivosBinarios.objects.get(ativo_binario='NZDUSD-OTC')

    logger.info('Ativo binário NZDUSD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('NZDUSD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para NZDUSD-OTC.')

    # Verifique se o ativo binário está aberto
    if not nzdusd_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('NZDUSD-OTC', 60)
        logger.info('Ativo binário NZDUSD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o NZDUSD-OTC
    candles = IQAPI.get_realtime_candles('NZDUSD-OTC', 60)

    logger.info('Informações das velas obtidas para NZDUSD-OTC.')

    # Crie um novo objeto CandlesNZDUSDotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesNZDUSDotc(
            ativo_binario=nzdusd_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesNZDUSDotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_nzdusdotc concluída.')

# USDBRL - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdbrl(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdbrl.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDBRL
    usdbrl = AtivosBinarios.objects.get(ativo_binario='USDBRL')

    logger.info('Ativo binário USDBRL obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDBRL', 60, 1)

    logger.info('Fluxo de velas iniciado para USDBRL.')

    # Verifique se o ativo binário está aberto
    if not usdbrl.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDBRL', 60)
        logger.info('Ativo binário USDBRL não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDBRL
    candles = IQAPI.get_realtime_candles('USDBRL', 60)

    logger.info('Informações das velas obtidas para USDBRL.')

    # Crie um novo objeto CandlesUSDBRL para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDBRL(
            ativo_binario=usdbrl,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDBRL salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdbrl concluída.')

# USDCAD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdcad(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdcad.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDCAD
    usdcad = AtivosBinarios.objects.get(ativo_binario='USDCAD')

    logger.info('Ativo binário USDCAD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDCAD', 60, 1)

    logger.info('Fluxo de velas iniciado para USDCAD.')

    # Verifique se o ativo binário está aberto
    if not usdcad.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDCAD', 60)
        logger.info('Ativo binário USDCAD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDCAD
    candles = IQAPI.get_realtime_candles('USDCAD', 60)

    logger.info('Informações das velas obtidas para USDCAD.')

    # Crie um novo objeto CandlesUSDCAD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDCAD(
            ativo_binario=usdcad,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDCAD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdcad concluída.')

# USDCHF - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdchf(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdchf.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDCHF
    usdchf = AtivosBinarios.objects.get(ativo_binario='USDCHF')

    logger.info('Ativo binário USDCHF obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDCHF', 60, 1)

    logger.info('Fluxo de velas iniciado para USDCHF.')

    # Verifique se o ativo binário está aberto
    if not usdchf.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDCHF', 60)
        logger.info('Ativo binário USDCHF não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDCHF
    candles = IQAPI.get_realtime_candles('USDCHF', 60)

    logger.info('Informações das velas obtidas para USDCHF.')

    # Crie um novo objeto CandlesUSDCHF para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDCHF(
            ativo_binario=usdchf,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDCHF salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdchf concluída.')

# USDCHF-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdchfotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdchfotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDCHF-OTC
    usdchf_otc = AtivosBinarios.objects.get(ativo_binario='USDCHF-OTC')

    logger.info('Ativo binário USDCHF-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDCHF-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDCHF-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdchf_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDCHF-OTC', 60)
        logger.info('Ativo binário USDCHF-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDCHF-OTC
    candles = IQAPI.get_realtime_candles('USDCHF-OTC', 60)

    logger.info('Informações das velas obtidas para USDCHF-OTC.')

    # Crie um novo objeto CandlesUSDCHFotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDCHFotc(
            ativo_binario=usdchf_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDCHFotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdchfotc concluída.')

# USDHKD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdhkd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdhkd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDHKD
    usdhkd = AtivosBinarios.objects.get(ativo_binario='USDHKD')

    logger.info('Ativo binário USDHKD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDHKD', 60, 1)

    logger.info('Fluxo de velas iniciado para USDHKD.')

    # Verifique se o ativo binário está aberto
    if not usdhkd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDHKD', 60)
        logger.info('Ativo binário USDHKD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDHKD
    candles = IQAPI.get_realtime_candles('USDHKD', 60)

    logger.info('Informações das velas obtidas para USDHKD.')

    # Crie um novo objeto CandlesUSDHKD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDHKD(
            ativo_binario=usdhkd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDHKD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdhkd concluída.')

# USDHKD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdhkdotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdhkdotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDHKD-OTC
    usdhkd_otc = AtivosBinarios.objects.get(ativo_binario='USDHKD-OTC')

    logger.info('Ativo binário USDHKD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDHKD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDHKD-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdhkd_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDHKD-OTC', 60)
        logger.info('Ativo binário USDHKD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDHKD-OTC
    candles = IQAPI.get_realtime_candles('USDHKD-OTC', 60)

    logger.info('Informações das velas obtidas para USDHKD-OTC.')

    # Crie um novo objeto CandlesUSDHKDotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDHKDotc(
            ativo_binario=usdhkd_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDHKDotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdhkdotc concluída.')

# USDINR - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdinr(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdinr.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDINR
    usdinr = AtivosBinarios.objects.get(ativo_binario='USDINR')

    logger.info('Ativo binário USDINR obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDINR', 60, 1)

    logger.info('Fluxo de velas iniciado para USDINR.')

    # Verifique se o ativo binário está aberto
    if not usdinr.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDINR', 60)
        logger.info('Ativo binário USDINR não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDINR
    candles = IQAPI.get_realtime_candles('USDINR', 60)

    logger.info('Informações das velas obtidas para USDINR.')

    # Crie um novo objeto CandlesUSDINR para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDINR(
            ativo_binario=usdinr,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDINR salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdinr concluída.')

# USDINR-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdinrotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdinrotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDINR-OTC
    usdinr_otc = AtivosBinarios.objects.get(ativo_binario='USDINR-OTC')

    logger.info('Ativo binário USDINR-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDINR-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDINR-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdinr_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDINR-OTC', 60)
        logger.info('Ativo binário USDINR-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDINR-OTC
    candles = IQAPI.get_realtime_candles('USDINR-OTC', 60)

    logger.info('Informações das velas obtidas para USDINR-OTC.')

    # Crie um novo objeto CandlesUSDINRotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDINRotc(
            ativo_binario=usdinr_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDINRotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdinrotc concluída.')

# USDJPY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdjpy(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdjpy.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDJPY
    usdjpy = AtivosBinarios.objects.get(ativo_binario='USDJPY')

    logger.info('Ativo binário USDJPY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDJPY', 60, 1)

    logger.info('Fluxo de velas iniciado para USDJPY.')

    # Verifique se o ativo binário está aberto
    if not usdjpy.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDJPY', 60)
        logger.info('Ativo binário USDJPY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDJPY
    candles = IQAPI.get_realtime_candles('USDJPY', 60)

    logger.info('Informações das velas obtidas para USDJPY.')

    # Crie um novo objeto CandlesUSDJPY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDJPY(
            ativo_binario=usdjpy,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDJPY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdjpy concluída.')

# USDJPY-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdjpyotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdjpyotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDJPY-OTC
    usdjpyotc = AtivosBinarios.objects.get(ativo_binario='USDJPY-OTC')

    logger.info('Ativo binário USDJPY-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDJPY-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDJPY-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdjpyotc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDJPY-OTC', 60)
        logger.info('Ativo binário USDJPY-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDJPY-OTC
    candles = IQAPI.get_realtime_candles('USDJPY-OTC', 60)

    logger.info('Informações das velas obtidas para USDJPY-OTC.')

    # Crie um novo objeto CandlesUSDJPYotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDJPYotc(
            ativo_binario=usdjpyotc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDJPYotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdjpyotc concluída.')

# USDNOK - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdnok(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdnok.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDNOK
    usdnok = AtivosBinarios.objects.get(ativo_binario='USDNOK')

    logger.info('Ativo binário USDNOK obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDNOK', 60, 1)

    logger.info('Fluxo de velas iniciado para USDNOK.')

    # Verifique se o ativo binário está aberto
    if not usdnok.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDNOK', 60)
        logger.info('Ativo binário USDNOK não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDNOK
    candles = IQAPI.get_realtime_candles('USDNOK', 60)

    logger.info('Informações das velas obtidas para USDNOK.')

    # Crie um novo objeto CandlesUSDNOK para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDNOK(
            ativo_binario=usdnok,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDNOK salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdnok concluída.')

# USDPLN - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdpln(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdpln.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDPLN
    usdpln = AtivosBinarios.objects.get(ativo_binario='USDPLN')

    logger.info('Ativo binário USDPLN obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDPLN', 60, 1)

    logger.info('Fluxo de velas iniciado para USDPLN.')

    # Verifique se o ativo binário está aberto
    if not usdpln.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDPLN', 60)
        logger.info('Ativo binário USDPLN não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDPLN
    candles = IQAPI.get_realtime_candles('USDPLN', 60)

    logger.info('Informações das velas obtidas para USDPLN.')

    # Crie um novo objeto CandlesUSDPLN para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDPLN(
            ativo_binario=usdpln,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDPLN salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdpln concluída.')

# USDRUB - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdrub(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdrub.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDRUB
    usdrub = AtivosBinarios.objects.get(ativo_binario='USDRUB')

    logger.info('Ativo binário USDRUB obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDRUB', 60, 1)

    logger.info('Fluxo de velas iniciado para USDRUB.')

    # Verifique se o ativo binário está aberto
    if not usdrub.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDRUB', 60)
        logger.info('Ativo binário USDRUB não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDRUB
    candles = IQAPI.get_realtime_candles('USDRUB', 60)

    logger.info('Informações das velas obtidas para USDRUB.')

    # Crie um novo objeto CandlesUSDRUB para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDRUB(
            ativo_binario=usdrub,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDRUB salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdrub concluída.')

# USDSEK - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdsek(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdsek.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDSEK
    usdsek = AtivosBinarios.objects.get(ativo_binario='USDSEK')

    logger.info('Ativo binário USDSEK obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDSEK', 60, 1)

    logger.info('Fluxo de velas iniciado para USDSEK.')

    # Verifique se o ativo binário está aberto
    if not usdsek.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDSEK', 60)
        logger.info('Ativo binário USDSEK não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDSEK
    candles = IQAPI.get_realtime_candles('USDSEK', 60)

    logger.info('Informações das velas obtidas para USDSEK.')

    # Crie um novo objeto CandlesUSDSEK para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDSEK(
            ativo_binario=usdsek,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDSEK salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdsek concluída.')

# USDSGD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdsgd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdsgd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDSGD
    usdsgd = AtivosBinarios.objects.get(ativo_binario='USDSGD')

    logger.info('Ativo binário USDSGD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDSGD', 60, 1)

    logger.info('Fluxo de velas iniciado para USDSGD.')

    # Verifique se o ativo binário está aberto
    if not usdsgd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDSGD', 60)
        logger.info('Ativo binário USDSGD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDSGD
    candles = IQAPI.get_realtime_candles('USDSGD', 60)

    logger.info('Informações das velas obtidas para USDSGD.')

    # Crie um novo objeto CandlesUSDSGD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDSGD(
            ativo_binario=usdsgd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDSGD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdsgd concluída.')

# USDSGD-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdsgdotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdsgdotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDSGD-OTC
    usdsgdotc = AtivosBinarios.objects.get(ativo_binario='USDSGD-OTC')

    logger.info('Ativo binário USDSGD-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDSGD-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDSGD-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdsgdotc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDSGD-OTC', 60)
        logger.info('Ativo binário USDSGD-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDSGD-OTC
    candles = IQAPI.get_realtime_candles('USDSGD-OTC', 60)

    logger.info('Informações das velas obtidas para USDSGD-OTC.')

    # Crie um novo objeto CandlesUSDSGDotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDSGDotc(
            ativo_binario=usdsgdotc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDSGDotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdsgdotc concluída.')

# USDTRY - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdtry(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdtry.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDTRY
    usdtry = AtivosBinarios.objects.get(ativo_binario='USDTRY')

    logger.info('Ativo binário USDTRY obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDTRY', 60, 1)

    logger.info('Fluxo de velas iniciado para USDTRY.')

    # Verifique se o ativo binário está aberto
    if not usdtry.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDTRY', 60)
        logger.info('Ativo binário USDTRY não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDTRY
    candles = IQAPI.get_realtime_candles('USDTRY', 60)

    logger.info('Informações das velas obtidas para USDTRY.')

    # Crie um novo objeto CandlesUSDTRY para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDTRY(
            ativo_binario=usdtry,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDTRY salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdtry concluída.')

# USDZAR - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdzar(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdzar.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDZAR
    usdzar = AtivosBinarios.objects.get(ativo_binario='USDZAR')

    logger.info('Ativo binário USDZAR obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDZAR', 60, 1)

    logger.info('Fluxo de velas iniciado para USDZAR.')

    # Verifique se o ativo binário está aberto
    if not usdzar.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDZAR', 60)
        logger.info('Ativo binário USDZAR não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDZAR
    candles = IQAPI.get_realtime_candles('USDZAR', 60)

    logger.info('Informações das velas obtidas para USDZAR.')

    # Crie um novo objeto CandlesUSDZAR para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDZAR(
            ativo_binario=usdzar,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDZAR salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdzar concluída.')

# USDZAR-OTC - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usdzarotc(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usdzarotc.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USDZAR-OTC
    usdzar_otc = AtivosBinarios.objects.get(ativo_binario='USDZAR-OTC')

    logger.info('Ativo binário USDZAR-OTC obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USDZAR-OTC', 60, 1)

    logger.info('Fluxo de velas iniciado para USDZAR-OTC.')

    # Verifique se o ativo binário está aberto
    if not usdzar_otc.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USDZAR-OTC', 60)
        logger.info('Ativo binário USDZAR-OTC não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USDZAR-OTC
    candles = IQAPI.get_realtime_candles('USDZAR-OTC', 60)

    logger.info('Informações das velas obtidas para USDZAR-OTC.')

    # Crie um novo objeto CandlesUSDZARotc para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSDZARotc(
            ativo_binario=usdzar_otc,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSDZARotc salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usdzarotc concluída.')

# USOUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_usousd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_usousd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para USOUSD
    usousd = AtivosBinarios.objects.get(ativo_binario='USOUSD')

    logger.info('Ativo binário USOUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('USOUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para USOUSD.')

    # Verifique se o ativo binário está aberto
    if not usousd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('USOUSD', 60)
        logger.info('Ativo binário USOUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o USOUSD
    candles = IQAPI.get_realtime_candles('USOUSD', 60)

    logger.info('Informações das velas obtidas para USOUSD.')

    # Crie um novo objeto CandlesUSOUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesUSOUSD(
            ativo_binario=usousd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesUSOUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_usousd concluída.')


# XAUUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_xauusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_xauusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para XAUUSD
    xauusd = AtivosBinarios.objects.get(ativo_binario='XAUUSD')

    logger.info('Ativo binário XAUUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('XAUUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para XAUUSD.')

    # Verifique se o ativo binário está aberto
    if not xauusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('XAUUSD', 60)
        logger.info('Ativo binário XAUUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o XAUUSD
    candles = IQAPI.get_realtime_candles('XAUUSD', 60)

    logger.info('Informações das velas obtidas para XAUUSD.')

    # Crie um novo objeto CandlesXAUUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesXAUUSD(
            ativo_binario=xauusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesXAUUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_xauusd concluída.')

# XRPUSD - Atualização de Candlesticks
@shared_task(bind=True)
def atualizar_candles_xrpusd(self, iqoption_record, IQAPI):
    logger.info('Iniciando a tarefa atualizar_candles_xrpusd.')

    # Verifique a conexão
    if not IQAPI.check_connect():
        logger.error('Não foi possível conectar ao IQAPI.')
        return

    logger.info('Conexão com IQAPI estabelecida.')

    # Obtenha o ativo binário para XRPUSD
    xrpusd = AtivosBinarios.objects.get(ativo_binario='XRPUSD')

    logger.info('Ativo binário XRPUSD obtido.')

    # Inicie o fluxo de velas
    IQAPI.start_candles_stream('XRPUSD', 60, 1)

    logger.info('Fluxo de velas iniciado para XRPUSD.')

    # Verifique se o ativo binário está aberto
    if not xrpusd.ativo_binario_aberto:
        # Pare o fluxo de velas e saia do loop se o ativo binário não estiver aberto
        IQAPI.stop_candles_stream('XRPUSD', 60)
        logger.info('Ativo binário XRPUSD não está aberto. Parando o fluxo de velas.')
        return

    # Obtenha as informações das velas para o XRPUSD
    candles = IQAPI.get_realtime_candles('XRPUSD', 60)

    logger.info('Informações das velas obtidas para XRPUSD.')

    # Crie um novo objeto CandlesXRPUSD para cada vela
    for timestamp in candles:
        candle = candles[timestamp]
        iqoption_record = CandlesXRPUSD(
            ativo_binario=xrpusd,
            candle_timestamp=timestamp,
            candle_open=candle['open'],
            candle_high=candle['max'],
            candle_low=candle['min'],
            candle_close=candle['close'],
            candle_volume=candle['volume'],
        )

        # Salve o novo objeto no banco de dados
        iqoption_record.save()

        logger.info(f'Objeto CandlesXRPUSD salvo para o timestamp {timestamp}.')

    logger.info('Tarefa atualizar_candles_xrpusd concluída.')
