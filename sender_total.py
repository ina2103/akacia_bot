from common import BOT_TOKEN
from common.constants import *
from common.functions import *
from datetime import date
from telegram.ext import Updater


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

sender = Updater(token=BOT_TOKEN, use_context=True)

print("Выбор данных...")

today = date.today()
month = today.month - 1 if today.month > 1 else 12
year = today.year if today.month > 1 else today.year - 1
data = read_pgsql(("select c.tenant_telegram, tenant_language, b.chat_id, n.balance::numeric, "
    "is_paying_utilities, apartment_number, service_id, summa::numeric from vw_charge c "
    "inner join vw_bot_subscriber b on c.tenant_telegram=b.tenant_telegram "
    "inner join vw_balance n on c.tenant_telegram=n.tenant_telegram "
    f" where charge_year = {today.year} and charge_month = {today.month}"
    " order by apartment_number, service_id"))

def aparment_data(apart, records, other, rent, total, lang):
    text = TEMPLATE_TOTAL[lang].format(apart, MONTHS[lang][today.month - 1], rent)
    if len(records) > 0:
        text += TEMPLATE_KOMMUNALKA_MONTH[lang].format( MONTHS[lang][month - 1])
        text += "".join(records) + "    " + TEMPLATE_KOMMUNALKA_SUM[lang].format(total)
    if len(other) > 0:
        text += TEMPLATE_OTHER_SERVICES[lang] + "".join(other)
    return text

print("Начинается отправка сообщений для подписчиков\n")

if not data.empty:
    records = []
    other = []
    rent = 0
    total = 0
    apart = -1
    tenant = ""
    lang = 0
    chat_id = 0
    balance = 0
    for row in data.itertuples():
        if tenant != row.tenant_telegram:
            if tenant != "":
                try:
                    telegram_send(sender.bot, chat_id, aparment_data(apart, records, other, rent, total, lang))
                    telegram_send(sender.bot, chat_id,
                        TEMPLATE_BALANCE[lang].format(balance, TEMPLATE_MINUS if balance < 0 else TEMPLATE_PLUS) + TEMPLATE_FOOTER[lang])
                    print("* {} — отправлено".format(tenant))
                except:
                    print(f"Ошибка отправки {tenant}")
                apart = -1
            tenant = row.tenant_telegram
            lang = int(LANGUAGES[row.tenant_language])
            chat_id = row.chat_id
            balance = row.balance
            try:
                telegram_send(sender.bot, chat_id, TEMPLATE_HEADER[lang])
            except:
                print(f"Ошибка отправки {tenant}")
        if row.apartment_number != apart:
            if apart != -1:
                try:
                    telegram_send(sender.bot, chat_id, aparment_data(apart, records, other, rent, total, lang))
                except:
                    print(f"Ошибка отправки {tenant}")
            apart = row.apartment_number
            records = []
            other = []
            rent = 0
            total = 0
        if row.is_paying_utilities or (row.service_id not in UTILITES_SERVICE_IDS):
            total += row.summa
        if row.service_id == RENT_SERVICE_ID:
            rent = row.summa
        else:
            if row.service_id in UTILITES_SERVICE_IDS:
                records.append("    " + TEMPLATE_KOMMUNALKA_ROW.format(TEMPLATE_SERVICES[row.service_id][lang], row.summa))
            else:
                other.append("    " + TEMPLATE_KOMMUNALKA_ROW.format(TEMPLATE_SERVICES[row.service_id][lang], row.summa))
    try:
        telegram_send(sender.bot, chat_id, aparment_data(apart, records, other, rent, total, lang))
        telegram_send(sender.bot, chat_id,
            TEMPLATE_BALANCE[lang].format(balance, TEMPLATE_MINUS if balance < 0 else TEMPLATE_PLUS) + TEMPLATE_FOOTER[lang])
    except:
        print(f"Ошибка отправки {tenant}")
    print("* {} — отправлено".format(tenant))

print("\nОтправка закончена")