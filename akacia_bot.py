from datetime import date
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

from common import BOT_TOKEN
from common.constants import *
from common.functions import *

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


def command_start(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if tenant is None:
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return

    query = f"call sp_insert_bot_subscriber ('{tenant_id}', {chat_id});"
    if exec_pgsql(query):
        text = TEMPLATE_START[tenant["lang"]]
        telegram_send(context.bot, chat_id, text)


def command_stop(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if (tenant is None):
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return

    query = f"call sp_delete_bot_subscriber ('{tenant_id}');"
    if exec_pgsql(query):
        text = TEMPLATE_STOP[tenant["lang"]]
        telegram_send(context.bot, chat_id, text)


def command_balance(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if (tenant is None):
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return
    data = read_pgsql(f"select balance::numeric AS balance from vw_balance where tenant_telegram = '{tenant_id}'")
    if not data.empty:
        for row in data.itertuples():
            text = TEMPLATE_BALANCE[tenant["lang"]].format(row.balance,
                TEMPLATE_MINUS if row.balance < 0 else TEMPLATE_PLUS)
            telegram_send(context.bot, chat_id, text)
    else:
        text = TEMPLATE_BALANCE[tenant["lang"]].format(0, "")
        telegram_send(context.bot, chat_id, text)


def command_listing(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if (tenant is None):
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return
    lang = tenant["lang"]
    context.user_data["lang"] = lang
    query = ("select distinct event_year from vw_listing "
        f"where tenant_telegram = '{tenant_id}' order by event_year desc limit 9")
    data = read_pgsql(query)
    if not data.empty:
        if (context.args is not None and len(context.args) != 0):
            update.message.text = context.args[0]
            return process__listing_year(update, context)
        if (data.shape[0] == 1):
            update.message.text = str(data.at[0, "event_year"])
            return process__listing_year(update, context)
        buttons = [row.event_year for row in data.itertuples()]
        reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
        text = TEMPLATE_SELECT_YEAR[lang]
        telegram_send(context.bot, chat_id, text, reply_markup=reply_markup)
        return WAITING_YEAR
    else:
        text = TEMPLATE_BILLS_NOT_FOUND[lang]
        telegram_send(context.bot, chat_id, text)
        return ConversationHandler.END


def process__listing_year(update: Update, context: CallbackContext):

    def compose_message(listing, year, apart, records, lang):
        # start_year = listing.query(f"event_year < {year} & apartment_number == {apart}")["summa"].sum()
        # end_year = listing.query(f"event_year <= {year} & apartment_number == {apart}")["summa"].sum()
        text = TEMPLATE_LISTING_START[lang].format(year) + \
            "\n".join(records)
            #TEMPLATE_LISTING_END[lang].format(year, end_year)
        return text

    param = update.message.text.replace("'", "")
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    year = date.today().year
    try:
        year = int(param)
    except ValueError:
        pass
    lang = context.user_data["lang"]
    history = read_pgsql(("select event_year, event_text_date, apartment_number, summa::numeric, summa2::numeric from vw_listing"
        f" where tenant_telegram = '{tenant_id}'"))
    listing = history.query(f"event_year == {year}") if not history.empty else pd.DataFrame()
    if not listing.empty:
        apart = -1
        records = []
        for row in listing.itertuples():
            if row.apartment_number != apart:
                if apart != -1:
                    text = compose_message(history, year, apart, records, lang)
                    telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
                apart = row.apartment_number
                records = []
            if row.summa2 != 0:
                temp = TEMPLATE_LISTING_BILL if row.summa < 0 else TEMPLATE_LISTING_PAYMENT
                records.append(temp.format(row.event_text_date, abs(row.summa)))
        text = compose_message(history, year, apart, records, lang)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_YEAR[lang]
        telegram_send(context.bot, chat_id, text)
        return WAITING_YEAR


def command_info(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if (tenant is None):
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return
    lang = tenant["lang"]
    context.user_data["lang"] = lang
    data = read_pgsql((f"select distinct charge_year, charge_month from vw_charge_extract where tenant_telegram = '{tenant_id}'"
        " order by charge_year desc, charge_month desc limit 9"))
    if not data.empty:
        buttons = [f"{MONTHS[lang][row.charge_month - 1]} {row.charge_year}" for row in data.itertuples()]
        reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
        if (context.args is not None and len(context.args) != 0):
            text = context.args[0]
            if (len(context.args) > 1):
                text += " " + context.args[1]
            else:
                text += " " + str(date.today().year)
            update.message.text = text
            return process__info_month(update, context)
        text = TEMPLATE_SELECT_MONTH[lang]
        telegram_send(context.bot, chat_id, text, reply_markup=reply_markup)
        return WAITING_MONTH
    else:
        text = TEMPLATE_BILLS_NOT_FOUND[lang]
        telegram_send(context.bot, chat_id, text)
        return ConversationHandler.END


def process__info_month(update: Update, context: CallbackContext):
    param = update.message.text.lower().replace("'", "").split(" ")
    if (len(param) == 1):
        param.append(str(date.today().year))
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    month = -1
    lang = context.user_data["lang"]
    try:
        month = [x.lower() for x in MONTHS[lang]].index(param[0]) + 1
        param[0] = MONTHS[lang][month - 1]
    except ValueError:
        pass
    data = read_pgsql(("select apartment_number, is_paying_utilities, service_id, summa::numeric from vw_charge_extract"
        f" where tenant_telegram = '{tenant_id}' and charge_year = {param[1]} and charge_month = {month}"
        " order by apartment_number, service_id"))
    if not data.empty:
        apart = -1
        records = []
        rent = 0
        total = 0
        for row in data.itertuples():
            if row.apartment_number != apart:
                if apart != -1:
                    text = TEMPLATE_INFO[lang].format(apart, " ".join(param), rent)
                    if len(records) > 0:
                        text += "".join(records) + TEMPLATE_KOMMUNALKA_SUM[lang].format(total)
                    telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
                apart = row.apartment_number
                records = []
                rent = 0
                total = 0
            if row.is_paying_utilities or (row.service_id not in UTILITES_SERVICE_IDS):
                total += row.summa
            if row.service_id == RENT_SERVICE_ID:
                rent = row.summa
            else:
                records.append(TEMPLATE_KOMMUNALKA_ROW.format(TEMPLATE_SERVICES[row.service_id][lang], row.summa))
        text = TEMPLATE_INFO[lang].format(apart, " ".join(param), rent)
        if len(records) > 0:
            text += "".join(records) + TEMPLATE_KOMMUNALKA_SUM[lang].format(total)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_MONTH[lang]
        telegram_send(context.bot, chat_id, text)
        return WAITING_MONTH

def command_exit(update: Update, context: CallbackContext):
    tenant_id = update.message.from_user.username
    chat_id = update.message.chat.id
    tenant = check_tenant(tenant_id)
    if (tenant is None):
        telegram_send(context.bot, chat_id, TEMPLATE_NOT_FOUND)
        return
    lang = tenant["lang"]
    telegram_send(context.bot, chat_id, TEMPLATE_EXIT_CONVERSATION[lang], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(COMMAND_START, command_start), 1)
    dispatcher.add_handler(CommandHandler(COMMAND_STOP, command_stop), 2)
    dispatcher.add_handler(CommandHandler(COMMAND_BOT_BALANCE, command_balance), 3)
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler(COMMAND_BOT_LISTING, command_listing)
        ],
        states={
            WAITING_YEAR: [MessageHandler(Filters.text & ~Filters.command, process__listing_year)]
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
    ), 4)
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler(COMMAND_BOT_INFO, command_info)
        ],
        states={
            WAITING_MONTH: [MessageHandler(Filters.text & ~Filters.command, process__info_month)]
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
    ), 5)

    print("Akacia bot started")

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
