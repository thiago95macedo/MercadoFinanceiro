from accounts.models import IQOption
from .tasks import login_iqoption, atualizar_ativos_binarios
from .tasks import atualizar_candles_audcad, atualizar_candles_audcadotc, atualizar_candles_audchf, atualizar_candles_audjpy, atualizar_candles_audnzd
from .tasks import atualizar_candles_audusd, atualizar_candles_btcusd, atualizar_candles_cadchf, atualizar_candles_cadjpy, atualizar_candles_chfjpy
from .tasks import atualizar_candles_eosusd, atualizar_candles_ethusd, atualizar_candles_euraud, atualizar_candles_eurcad, atualizar_candles_eurchf
from .tasks import atualizar_candles_eurgbp, atualizar_candles_eurgbpotc, atualizar_candles_eurjpy, atualizar_candles_eurjpyotc, atualizar_candles_eurnzd
from .tasks import atualizar_candles_eurusd, atualizar_candles_eurusdotc, atualizar_candles_gbpaud, atualizar_candles_gbpcad, atualizar_candles_gbpchf
from .tasks import atualizar_candles_gbpjpy, atualizar_candles_gbpjpyotc, atualizar_candles_gbpnzd, atualizar_candles_gbpusd, atualizar_candles_gbpusdotc
from .tasks import atualizar_candles_ltcusd, atualizar_candles_nzdusd, atualizar_candles_nzdusdotc, atualizar_candles_usdbrl, atualizar_candles_usdcad
from .tasks import atualizar_candles_usdchf, atualizar_candles_usdchfotc, atualizar_candles_usdhkd, atualizar_candles_usdhkdotc, atualizar_candles_usdinr
from .tasks import atualizar_candles_usdinrotc, atualizar_candles_usdjpy, atualizar_candles_usdjpyotc, atualizar_candles_usdnok, atualizar_candles_usdpln
from .tasks import atualizar_candles_usdrub, atualizar_candles_usdsek, atualizar_candles_usdsgd, atualizar_candles_usdsgdotc, atualizar_candles_usdtry
from .tasks import atualizar_candles_usdzar, atualizar_candles_usdzarotc, atualizar_candles_usousd, atualizar_candles_xauusd, atualizar_candles_xrpusd


import logging

logger = logging.getLogger(__name__)

# Cron Job: Atualizar Ativos Binários
def cron_atualizar_ativos_binarios():
    iqoption_record_pass = IQOption.objects.get(id=1)  # Substitua 1 pelo ID do seu iqoption_record
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_ativos_binarios(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDCAD
def cron_atualizar_candles_audcad():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audcad(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDCAD-OTC
def cron_atualizar_candles_audcadotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audcadotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDCHF
def cron_atualizar_candles_audchf():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audchf(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDJPY
def cron_atualizar_candles_audjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDNZD
def cron_atualizar_candles_audnzd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audnzd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles AUDUSD
def cron_atualizar_candles_audusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_audusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles BTCUSD
def cron_atualizar_candles_btcusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_btcusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles CADCHF
def cron_atualizar_candles_cadchf():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_cadchf(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles CADJPY
def cron_atualizar_candles_cadjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_cadjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles CHFJPY
def cron_atualizar_candles_chfjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_chfjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EOSUSD
def cron_atualizar_candles_eosusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eosusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles ETHUSD
def cron_atualizar_candles_ethusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_ethusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURAUD
def cron_atualizar_candles_euraud():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_euraud(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURCAD
def cron_atualizar_candles_eurcad():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurcad(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURCHF
def cron_atualizar_candles_eurchf():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurchf(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURGBP
def cron_atualizar_candles_eurgbp():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurgbp(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURGBP-OTC
def cron_atualizar_candles_eurgbpotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurgbpotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURJPY
def cron_atualizar_candles_eurjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURJPY-OTC
def cron_atualizar_candles_eurjpyotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurjpyotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURNZD
def cron_atualizar_candles_eurnzd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurnzd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURUSD
def cron_atualizar_candles_eurusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles EURUSD-OTC
def cron_atualizar_candles_eurusdotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_eurusdotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPAUD
def cron_atualizar_candles_gbpaud():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpaud(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPCAD
def cron_atualizar_candles_gbpcad():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpcad(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPCHF
def cron_atualizar_candles_gbpchf():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpchf(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPJPY
def cron_atualizar_candles_gbpjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPJPY-OTC
def cron_atualizar_candles_gbpjpyotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpjpyotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPNZD
def cron_atualizar_candles_gbpnzd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpnzd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPUSD
def cron_atualizar_candles_gbpusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles GBPUSD-OTC
def cron_atualizar_candles_gbpusdotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_gbpusdotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles LTCUSD
def cron_atualizar_candles_ltcusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_ltcusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles NZDUSD
def cron_atualizar_candles_nzdusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_nzdusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles NZDUSD-OTC
def cron_atualizar_candles_nzdusdotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_nzdusdotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDBRL
def cron_atualizar_candles_usdbrl():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdbrl(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDCAD
def cron_atualizar_candles_usdcad():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdcad(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDCHF
def cron_atualizar_candles_usdchf():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdchf(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDCHFotc
def cron_atualizar_candles_usdchfotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdchfotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDHKD
def cron_atualizar_candles_usdhkd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdhkd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDHKDotc
def cron_atualizar_candles_usdhkdotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdhkdotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDINR
def cron_atualizar_candles_usdinr():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdinr(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDINRotc
def cron_atualizar_candles_usdinrotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdinrotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDJPY
def cron_atualizar_candles_usdjpy():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdjpy(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDJPYotc
def cron_atualizar_candles_usdjpyotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdjpyotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDNOK
def cron_atualizar_candles_usdnok():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdnok(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDPLN
def cron_atualizar_candles_usdpln():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdpln(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDRUB
def cron_atualizar_candles_usdrub():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdrub(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDSEK
def cron_atualizar_candles_usdsek():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdsek(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDSGD
def cron_atualizar_candles_usdsgd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdsgd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDSGDotc
def cron_atualizar_candles_usdsgdotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdsgdotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDTRY
def cron_atualizar_candles_usdtry():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdtry(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDZAR
def cron_atualizar_candles_usdzar():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdzar(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USDZARotc
def cron_atualizar_candles_usdzarotc():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usdzarotc(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles USOUSD
def cron_atualizar_candles_usousd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_usousd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles XAUUSD
def cron_atualizar_candles_xauusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_xauusd(iqoption_record_pass, IQAPI)

# Cron Job: Atualizar Candles XRPUSD
def cron_atualizar_candles_xrpusd():
    iqoption_record_pass = IQOption.objects.get(id=1)
    IQAPI = login_iqoption(iqoption_record_pass)
    atualizar_candles_xrpusd(iqoption_record_pass, IQAPI)
