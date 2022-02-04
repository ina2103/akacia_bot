from copyreg import pickle
from datetime import date, timedelta
from random import choice

from yaml import add_path_resolver
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
import traceback
import re

from common import AOT_TOKEN, BOT_TOKEN
from common.constants import *
from common.functions import *

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)


updater = None
ROUTES = {}

# Commands

def command_start(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, "start")
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return

    query = f"call sp_insert_aot_subscriber ('{staff_id}', {chat_id});"
    if exec_pgsql(query):
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_FOUND)


def command_add(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_ADD)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_ADD
    if not context.args or len(context.args) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return process__apart(update, context)


def command_balance(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_BALANCE)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_BALANCE
    if not context.args or len(context.args) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return process__apart(update, context)


def command_debtors(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_DEBTORS)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return process__debtors(update, context)


def command_debtors_no_balance(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_DEBTORS_NO_BALANCE)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return process__debtors_no_balance(update, context)


def command_exit(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    telegram_send(context.bot, chat_id, TEMPLATE_EXIT_CONVERSATION[LANGUAGE_RU], reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def command_free_apart(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_FREE_APART)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return process__free_apart(update, context)


def command_info(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_INFO)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_INFO
    if not context.args or len(context.args) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return process__apart(update, context)


def command_listing(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_LISTING)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_LISTING
    if not context.args or len(context.args) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return process__apart(update, context)


def command_living(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    context.user_data["stay_type"] = "long"
    staff = check_staff(staff_id, COMMAND_AOT_LIVING)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_LIVING
    return conversation__tenant_telegram  (update, context)


def command_out(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_OUT)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_OUT
    if not context.args or len(context.args) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return process__apart(update, context)


def command_send (update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_SEND)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return conversation__send(update, context)


def command_short_stay(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_SHORT_STAY)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    context.user_data["route"] = COMMAND_AOT_SHORT_STAY
    return conversation__short_stay_first_name(update, context)


def command_state(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_STATE)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return conversation__state(update, context)


def command_new_tenant(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_TENANT)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    return conversation__tenant_telegram(update, context)


def command_transfer(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_TRANSFER)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    cashboxes = select_allowed_cashboxes(staff_id)
    cashboxes_from = [cashbox for cashbox in cashboxes if cashbox["cashbox_is_cash"] and cashbox["can_transfer_from"]]
    cashboxes_to = [cashbox for cashbox in cashboxes if cashbox["cashbox_is_cash"] and cashbox["can_transfer_to"]]
    buttons = [[f'{x["cashbox_name"]} > {y["cashbox_name"]}'] for x in cashboxes_from for y in cashboxes_to \
                if x["cashbox_name"] != y["cashbox_name"]]
    if (len(context.args) == 1):
        from_cashbox = next((cashbox for cashbox in cashboxes_from if cashbox["cashbox_name"]=="anna"), None)
        to_cashbox = next((cashbox for cashbox in cashboxes_to if cashbox["cashbox_name"]=="mike"), None)
        if (from_cashbox is not None) and (to_cashbox is not None):
            context.user_data["from_cashbox"] = from_cashbox
            context.user_data["to_cashbox"] = to_cashbox
            update.message.text = context.args[0]
            return conversation__transfer_sum(update, context)
    if len(buttons) == 1:
        update.message.text = buttons[0][0]
        return conversation__transfer_cashboxes(update, context)
    if len(buttons) > 1:
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        telegram_send(context.bot, chat_id, TEMPLATE_SELECT_CASHBOXES, reply_markup=reply_markup)
        return WAITING_CASHBOX

    telegram_send(context.bot, chat_id, TEMPLATE_NO_CASHBOXES)
    return ConversationHandler.END


def command_upload(update: Update, context: CallbackContext):
    staff_id = update.message.from_user.username
    chat_id = update.message.chat.id
    staff = check_staff(staff_id, COMMAND_AOT_UPLOAD)
    if not staff:
        telegram_send(context.bot, chat_id, TEMPLATE_MANAGER_NO_PERMISSION)
        return ConversationHandler.END
    buttons = [TEMPLATE_SERVICES[i][LANGUAGE_RU] for i in UTILITES_SERVICE_IDS]
    reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
    telegram_send(context.bot, chat_id, TEMPLATE_UPLOAD_SELECT_SERVICE, reply_markup=reply_markup)
    return WAITING_SERVICE


# Conversations

def conversation__add_sum(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    telegram_send(context.bot, chat_id, TEMPLATE_SEND_SUM.format(tenant_name, apart), reply_markup=ReplyKeyboardRemove())
    return WAITING_SUM


def conversation__info_month(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    tenant_telegram = context.user_data["tenant_telegram"]
    lang = LANGUAGE_RU
    data = read_pgsql(("select distinct charge_year, charge_month from vw_charge_extract "
        f"where tenant_telegram = '{tenant_telegram}' and apartment_number={apart} "
        "order by charge_year desc, charge_month desc limit 12"))
    if not data.empty:
        buttons = [f"{MONTHS[lang][row.charge_month - 1]} {row.charge_year}" for row in data.itertuples()]
        reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
        text = TEMPLATE_SELECT_MONTH[lang]
        telegram_send(context.bot, chat_id, text, reply_markup=reply_markup)
        return WAITING_MONTH
    else:
        text = TEMPLATE_BILLS_NOT_FOUND[lang]
        telegram_send(context.bot, chat_id, text)
        return ConversationHandler.END


def conversation__listing_year(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    tenant_telegram = context.user_data["tenant_telegram"]
    lang = LANGUAGE_RU
    data = read_pgsql(("select distinct event_year from vw_listing "
        f"where tenant_telegram = '{tenant_telegram}' and apartment_number={apart} "
        "order by event_year desc limit 9"))
    if not data.empty:
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


def conversation__out(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    data = read_pgsql(f"select tenant_full_name, living_start_date, tenant_telegram from vw_actual_apartment_tenant where apartment_id = {apart} AND tenant_id != 0")
    if data.empty:
        text = TEMPLATE_NO_TENANT.format(apart) + TEMPLATE_SEND_APART
        telegram_send(context.bot, chat_id, text)
        return WAITING_APART
    tenant = data["tenant_full_name"].values[0]
    context.user_data["living_start_date"] = data["living_start_date"].values[0]
    context.user_data["tenant_name"] = tenant
    context.user_data["tenant_telegram"] = data["tenant_telegram"].values[0]
    text = TEMPLATE_TENANT_OUT.format(tenant, apart)
    reply_markup = ReplyKeyboardMarkup([[TEMPLATE_YES, TEMPLATE_NO]], resize_keyboard=True)
    telegram_send(context.bot, chat_id, text, reply_markup)
    return WAITING_YES_NO


def conversation__list_tenants(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    route = context.user_data["route"]
    if route in []:
        query = ("select tenant_full_name from vw_living "
            f"where tenant_id != 0 and apartment_number={apart} and living_end_date is null "
            "order by living_start_date desc limit 12")
    else:
        query = ("select tenant_full_name from vw_living "
            f"where tenant_id != 0 and apartment_number={apart} "
            "order by living_start_date desc limit 12")
    data = read_pgsql(query)
    if data.empty:
        telegram_send(context.bot, chat_id, f"{TEMPLATE_ERROR_IN_APART}\n{TEMPLATE_SEND_APART}")
        return WAITING_APART
    data.drop_duplicates(inplace=True)
    if data.shape[0] == 1:
        update.message.text = data["tenant_full_name"].values[0]
        return process__tenant(update, context)
    buttons = [row.tenant_full_name for row in data.itertuples()]
    reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
    telegram_send(context.bot, chat_id, TEMPLATE_SEND_TENANT.format(apart), reply_markup=reply_markup)
    return WAITING_TENANT


def conversation__send(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    buttons = [[c] for c in SEND_OPTIONS]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    telegram_send(context.bot, chat_id, TEMPLATE_SEND, reply_markup=reply_markup)
    return WAITING_CHOICE


def conversation__short_stay_first_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    telegram_send(context.bot, chat_id, TEMPLATE_TENANT_NAME)
    return WAITING_TENANT_NAME


def conversation__short_stay_last_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.user_data["tenant_first_name"] = update.message.text.replace("'", "")
    telegram_send(context.bot, chat_id, TEMPLATE_TENANT_LASTNAME)
    return WAITING_TENANT_LASTNAME


def conversation__short_stay_apart(update: Update, context: CallbackContext):
    context.user_data["tenant_last_name"] = update.message.text.replace("'", "")
    context.user_data["stay_type"] = "short"
    return process__select_free_apart(update, context)


def conversation__short_stay_length(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    telegram_send(context.bot, chat_id, TEMPLATE_LIVING_DAYS)
    return WAITING_LENGTH


def conversation__state(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    lang = LANGUAGE_RU
    data = read_pgsql(("select distinct charge_year, charge_month from vw_charge_extract "
        "order by charge_year desc, charge_month desc limit 12"))
    if not data.empty:
        buttons = [f"{MONTHS[lang][row.charge_month - 1]} {row.charge_year}" for row in data.itertuples()]
        reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard(buttons), resize_keyboard=True)
        text = TEMPLATE_SELECT_MONTH[lang]
        telegram_send(context.bot, chat_id, text, reply_markup=reply_markup)
        return WAITING_MONTH
    else:
        return ConversationHandler.END


def conversation__tenant_telegram(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = TEMPLATE_TENANT_TELEGRAM
    telegram_send(context.bot, chat_id, text)
    return WAITING_CONTACT


def conversation__select_tenant(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    contact = update.message.contact
    try:
        user_data = context.bot.get_chat(contact.user_id)
    except:
        user_data = None
    if user_data is None or user_data.username is None or user_data.username == "":
        telegram_send(context.bot, chat_id, TEMPLATE_TENANT_TELEGRAM_NONE)
        return ConversationHandler.END
    context.user_data["tenant_telegram"] = user_data.username
    query = f"select tenant_id, tenant_full_name from vw_tenant where tenant_telegram = '{user_data.username}'"
    data = read_pgsql(query)
    if not data.empty:
        tenant_full_name = data["tenant_full_name"].values[0]
        context.user_data["tenant_full_name"] = tenant_full_name
        context.user_data["tenant_id"] = data["tenant_id"].values[0]
        return process__select_free_apart(update, context)
    else:
        telegram_send(context.bot, chat_id, TEMPLATE_TENANT_NOT_FOUND)
        return ConversationHandler.END


def conversation__new_tenant_first_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    contact = update.message.contact
    try:
        user_data = context.bot.get_chat(contact.user_id)
    except:
        user_data = None
    if user_data is None or user_data.username is None or user_data.username == "":
        telegram_send(context.bot, chat_id, TEMPLATE_TENANT_TELEGRAM_NONE)
        return ConversationHandler.END
    context.user_data["tenant_telegram"] = user_data.username
    context.user_data["tenant_first_name"] = user_data.first_name
    context.user_data["tenant_last_name"] = user_data.last_name
    reply_markup = ReplyKeyboardMarkup([[user_data.first_name]], resize_keyboard=True) if user_data.first_name != "" \
        else ReplyKeyboardRemove()
    telegram_send(context.bot, chat_id, TEMPLATE_TENANT_NAME, reply_markup=reply_markup)
    return WAITING_TENANT_NAME


def conversation__new_tenant_last_name(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.user_data["tenant_first_name"] = update.message.text
    reply_markup = ReplyKeyboardMarkup([[context.user_data["tenant_last_name"]]], resize_keyboard=True) if context.user_data["tenant_last_name"] != "" \
        else ReplyKeyboardRemove()
    telegram_send(context.bot, chat_id, TEMPLATE_TENANT_LASTNAME, reply_markup=reply_markup)
    return WAITING_TENANT_LASTNAME


def conversation__new_tenant_language(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.user_data["tenant_last_name"] = update.message.text
    telegram_send(context.bot, chat_id, TEMPLATE_TENANT_LANGUAGE, 
        reply_markup=ReplyKeyboardMarkup([[n for n in LANGUAGES]], resize_keyboard=True))
    return WAITING_TENANT_LANGUAGE


def conversation__transfer_cashboxes(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_id = update.message.from_user.username
    params = update.message.text.split(" > ")
    cashboxes = select_allowed_cashboxes(staff_id)
    from_cashbox = next((cashbox for cashbox in cashboxes if cashbox["cashbox_name"]==params[0] and cashbox["can_transfer_from"]), None)
    to_cashbox = next((cashbox for cashbox in cashboxes if cashbox["cashbox_name"]==params[1] and cashbox["can_transfer_to"]), None)
    if from_cashbox is None or to_cashbox is None:
        telegram_send(context.bot, chat_id, TEMPLATE_SELECT_CASHBOXES)
        return WAITING_CASHBOX
    context.user_data["from_cashbox"] = from_cashbox
    context.user_data["to_cashbox"] = to_cashbox
    telegram_send(context.bot, chat_id,
        TEMPLATE_SUM_TO_TRANSFER.format(params[0], params[1],
        context.user_data["from_cashbox"]["cashbox_name"], context.user_data["from_cashbox"]["balance"]),
        reply_markup=ReplyKeyboardRemove())
    return WAITING_SUM


def conversation__transfer_sum(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    summa = 0
    try:
        summa = int(update.message.text)
    except ValueError:
        pass
    if summa == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_SUM[:TEMPLATE_ERROR_SUM.find(" [")])
        return WAITING_SUM
    if summa > context.user_data["from_cashbox"]["balance"]:
        telegram_send(context.bot, chat_id, TEMPLATE_TRANSFER_ERROR.format(context.user_data["from_cashbox"]["cashbox_name"], 
            context.user_data["to_cashbox"]["cashbox_name"], context.user_data["from_cashbox"]["cashbox_name"],
            context.user_data["from_cashbox"]["balance"]), reply_markup=ReplyKeyboardRemove())
        return WAITING_SUM
    context.user_data["summa"] = summa
    return process__transfer_money(update, context)


def conversation__upload_select_service(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    context.user_data["service"] = update.message.text
    telegram_send(context.bot, chat_id, TEMPLATE_UPLOAD_SEND_FILE, reply_markup=ReplyKeyboardRemove())
    return WAITING_FILE


# Processes

def process__apart(update: Update, context: CallbackContext):
    apart = None
    chat_id = update.message.chat.id
    try:
        apart = int(update.message.text)
    except ValueError:
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return ConversationHandler.END
    context.user_data["apart"] = apart
    possible_routes = ROUTES["process__apart"]
    route = context.user_data["route"]
    if route in possible_routes:
        return possible_routes[route](update, context)
    else:
        log_error(f"Route '{route}' not found in possible routes")
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__add_sum(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_telegram = update.message.from_user.username
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    m = re.fullmatch(SUM_REGEX, update.message.text)
    if m is None:
        telegram_send(context.bot, chat_id, f"{TEMPLATE_ERROR_SUM}\n{TEMPLATE_SEND_SUM.format(tenant_name, apart)}")
        return WAITING_SUM
    try:
        d = m.groupdict("")
        payment_recieved = float(d["payment_recieved"])
        payment_saved = payment_recieved
        comment = ""
        if ("payment_saved" in d) and (d["payment_saved"] != "-") and (d["payment_saved"] != ""):
            payment_saved = float(d["payment_saved"])
        if "comment" in d:
            comment = d["comment"]
    except Exception as e:
        log_error(f"Error in parsing sum: {str(e)}")
        telegram_send(context.bot, chat_id, f"{TEMPLATE_ERROR_SUM}\n{TEMPLATE_SEND_SUM.format(tenant_name, apart)}")
        return WAITING_SUM

    context.user_data["payment_recieved"] = payment_recieved
    context.user_data["payment_saved"] = payment_saved
    context.user_data["comment"] = comment.replace("'", "''")

    cashboxes = select_allowed_cashboxes(staff_telegram)
    cash = [cashbox["cashbox_name"] for cashbox in cashboxes if cashbox["cashbox_is_cash"] and cashbox["can_add_to"]]
    if len(cash) > 1:
        buttons = [[x] for x in cash]
        reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        telegram_send(context.bot, chat_id, TEMPLATE_SELECT_CASHBOX, reply_markup=reply_markup)
        return WAITING_CASHBOX

    if len(cash) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_NO_CASHBOXES)
        return ConversationHandler.END

    update.message.text = cash[0]
    return process__add_cashbox(update, context)


def process__add_cashbox(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_telegram = update.message.from_user.username
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    payment_recieved = context.user_data["payment_recieved"]
    payment_saved = context.user_data["payment_saved"]

    cashboxes = select_allowed_cashboxes(staff_telegram)
    cash = [cashbox["cashbox_id"] for cashbox in cashboxes
        if cashbox["cashbox_is_cash"] and (cashbox["cashbox_name"] == update.message.text)]
    if len(cash) == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_NO_CASHBOXES)
        return ConversationHandler.END

    context.user_data["cashbox_id"] = cash[0]

    telegram_send(context.bot, chat_id, TEMPLATE_CONFIRM_SUM.format(payment_recieved, payment_saved, tenant_name, apart),
        reply_markup=ReplyKeyboardMarkup([[TEMPLATE_YES, TEMPLATE_NO]], resize_keyboard=True))
    return WAITING_CONFIRM_SUM


def process__add_confirm_sum(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_telegram = update.message.from_user.username
    apart = context.user_data["apart"]
    living_id = context.user_data["living_id"]
    tenant_name = context.user_data["tenant_name"]
    tenant_telegram = context.user_data["tenant_telegram"]
    payment_recieved = context.user_data["payment_recieved"]
    payment_saved = context.user_data["payment_saved"]
    comment = context.user_data["comment"]
    cashbox_id = context.user_data["cashbox_id"]
    confirm = update.message.text.lower()
    if (confirm != TEMPLATE_YES.lower()):
        telegram_send(context.bot, chat_id, TEMPLATE_SEND_SUM.format(tenant_name, apart), reply_markup=ReplyKeyboardRemove())
        return WAITING_SUM
    query = (f"call sp_insert_payment (null::smallint, {living_id}::smallint, {payment_recieved}, {payment_saved}, "
        f"'{comment}'::character varying, '{staff_telegram}'::character varying, {cashbox_id}::smallint);")
    if exec_pgsql(query):
        telegram_send(context.bot, chat_id, TEMPLATE_DATA_SAVED.format(payment_recieved, payment_saved, tenant_name, apart),
            reply_markup=ReplyKeyboardRemove())
        tenant = check_tenant(tenant_telegram)
        if (tenant is not None) and (tenant["chat_id"] != 0) and (payment_recieved != 0):
            sender = Updater(token=BOT_TOKEN, use_context=True)
            telegram_send(sender.bot, tenant["chat_id"], TEMPLATE_PAYMENT_ACCEPTED[tenant["lang"]].format(payment_recieved, apart))
            telegram_send(context.bot, chat_id, TEMPLATE_DATA_SENDED.format(tenant_telegram))

    return ConversationHandler.END


def process__balance(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    tenant_telegram = context.user_data["tenant_telegram"]
    data = read_pgsql(f"select balance::numeric, apartment_number from vw_balance_by_apartment where tenant_telegram = '{tenant_telegram}'")
    if not data.empty:
        total_balance = data["balance"].sum()
        if total_balance != 0:
            total_balance = f"+{total_balance:.2f}" if total_balance > 0 else f"−{abs(total_balance):.2f}"
        balance = data.query(f"apartment_number == {apart}")["balance"].sum()
        if balance != 0:
            balance = f"+{balance:.2f}" if balance > 0 else f"−{abs(balance):.2f}"
        text = TEMPLATE_BALANCE_ADM.format(tenant_name, apart, balance) + \
            (TEMPLATE_BALANCE_ADM_TOTAL.format(total_balance) if total_balance != balance else "")
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
    else:
        text = TEMPLATE_BALANCE_ADM.format(tenant_name, apart, 0)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def process__debtors(update: Update, context: CallbackContext):
    year = date.today().year
    month = MONTHS[LANGUAGE_RU][date.today().month - 1]
    chat_id = update.message.chat.id
    data = read_pgsql(f"select apartment_id, tenant_full_name, tenant_telegram, balance::numeric from vw_debtors")
    if not data.empty:
        records = []
        for row in data.itertuples():
            records.append(TEMPLATE_DEBTORS_ROW.format(row. apartment_id, row.tenant_full_name, row.tenant_telegram, row.balance))
        text = TEMPLATE_DEBTORS_ADM.format(month, year)
        if len(records) > 0:
            text += "".join(records)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__debtors_no_balance(update: Update, context: CallbackContext):
    year = date.today().year
    month = MONTHS[LANGUAGE_RU][date.today().month - 1]
    chat_id = update.message.chat.id
    data = read_pgsql(f"select apartment_id, tenant_full_name, tenant_telegram from vw_debtors")
    if not data.empty:
        records = []
        for row in data.itertuples():
            records.append(TEMPLATE_DEBTORS_NO_BALANCE_ROW.format(row. apartment_id, row.tenant_full_name, row.tenant_telegram))
        text = TEMPLATE_DEBTORS_ADM.format(month, year)
        if len(records) > 0:
            text += "".join(records)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__free_apart(update: Update, context: CallbackContext): 
    chat_id = update.message.chat.id
    data = read_pgsql(("SELECT DISTINCT apartment_type_name, apartment_floor,"
        "ARRAY_TO_STRING(ARRAY(SELECT apartment_number FROM vw_free_apartment b WHERE a.apartment_floor = b.apartment_floor "
        "AND a.apartment_type_name = b.apartment_type_name), ', ', '') as apart "
        "FROM vw_free_apartment a"))
    if not data.empty:
        records = []
        apartment_type = ''
        for row in data.itertuples():
            if apartment_type != row.apartment_type_name:
                records.append(TEMPLATE_FREE_APART_ADM.format(row.apartment_type_name))
                apartment_type = row.apartment_type_name
            records.append(TEMPLATE_FREE_APART_ROW.format(row.apartment_floor, row.apart))
        text = 'Нет свободных квартир'
        if len(records) > 0:
            text = "".join(records)
        telegram_send(context.bot, chat_id, TEMPLATE_FREE_APART_HEADER + text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__select_free_apart(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    process__free_apart(update, context)
    data = read_pgsql(f"select apartment_number from vw_free_apartment order by apartment_number")
    if data.empty:
        return ConversationHandler.END
    free_aparts = data["apartment_number"].values
    reply_markup = ReplyKeyboardMarkup(telegram_create_keyboard([str(a) for a in free_aparts]), resize_keyboard=True)
    context.user_data["free_aparts"] = free_aparts
    telegram_send(context.bot, chat_id, TEMPLATE_SHORT_STAY_APART, reply_markup)
    return WAITING_APART


def process__check_free_apart(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    if apart not in context.user_data["free_aparts"]: 
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return WAITING_APART
    if context.user_data["stay_type"] == "short":
        query = (f"select price_short_stay_price::numeric as price from vw_price_short_stay where apartment_type_name = "
            f"(select apartment_type_name from vw_free_apartment where apartment_number = {apart}) "
            f"and price_short_stay_month = extract (month from CURRENT_DATE)")
    else:
        query = (f"select price_long_stay::numeric as price from vw_price where apartment_type_name = "
            f"(select apartment_type_name from vw_free_apartment where apartment_number = {apart})")
    data = read_pgsql(query)
    if data.empty:
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return WAITING_APART
    telegram_send(context.bot, chat_id, TEMPLATE_LIVING_PRICE.format(data["price"].values[0]), reply_markup=ReplyKeyboardRemove())
    return WAITING_PRICE


def process__file(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    file = context.bot.getFile(update.message.document.file_id)
    service_id = 0
    for i in UTILITES_SERVICE_IDS:
        if TEMPLATE_SERVICES[i][LANGUAGE_RU] == context.user_data["service"]:
            service_id = i
            break
    if service_id == 0:
        telegram_send(context.bot, chat_id, TEMPLATE_UPLOAD_SELECT_SERVICE)
        return WAITING_SERVICE
    file.download("data.csv")
    try:
        df = pd.read_csv("./data.csv", sep="\t", header=0, names=["id", "summa"], dtype=str)
        df["summa"] = df["summa"].apply(lambda x: x.replace(",", ".")).astype(float)
        rows = []
        today = date.today()
        m = today.month - 2 if today.month > 1 else 11
        y = today.year if today.month > 1 else today.year - 1
        month = f"{MONTHS[LANGUAGE_RU][m].capitalize()} {y}"
        for row in df.itertuples():
            rows.append(f"({service_id}, '{row.id}', '{month}', {row.summa}),")
        query = f"DELETE FROM parsing WHERE parsing_period='{month}' and service_id={service_id};\n"
        query += "INSERT INTO parsing (service_id, parsing_counter, parsing_period, parsing_summa) VALUES\n" + \
            "\n".join(rows)[:-1] + ";"
        if exec_pgsql(query):
            query = f"call sp_insert_charge_from_parsing ({service_id}::smallint, '{y}-{m+1:02d}-01', '{update.message.from_user.username}');"
            if exec_pgsql(query):
                telegram_send(context.bot, chat_id, TEMPLATE_UPLOAD_SUCCESS)
                return ConversationHandler.END
    except Exception as e:
        log_error(f"Error in parsing file: {str(e)}")
    telegram_send(context.bot, chat_id, TEMPLATE_UPLOAD_ERROR)
    return ConversationHandler.END


def process__info_month(update: Update, context: CallbackContext):
    param = update.message.text.lower().replace("'", "").split(" ")
    if (len(param) == 1):
        param.append(str(date.today().year))
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    tenant_telegram = context.user_data["tenant_telegram"]
    chat_id = update.message.chat.id
    month = -1
    lang = LANGUAGE_RU
    try:
        month = [x.lower() for x in MONTHS[lang]].index(param[0]) + 1
        param[0] = MONTHS[lang][month - 1]
    except ValueError:
        pass
    data = read_pgsql(("select is_paying_utilities, service_id, summa::numeric from vw_charge_extract"
        f" where tenant_telegram = '{tenant_telegram}' and charge_year = {param[1]} and charge_month = {month} and apartment_number={apart}"
        " order by apartment_number, service_id"))
    if not data.empty:
        records = []
        rent = 0
        total = 0
        for row in data.itertuples():
            if row.is_paying_utilities or (row.service_id not in UTILITES_SERVICE_IDS):
                total += row.summa
            if row.service_id == RENT_SERVICE_ID:
                rent = row.summa
            else:
                records.append(TEMPLATE_KOMMUNALKA_ROW.format(TEMPLATE_SERVICES[row.service_id][lang], row.summa))
        text = TEMPLATE_INFO_ADM.format(tenant_name, apart, " ".join(param), rent)
        if len(records) > 0:
            text += "".join(records) + TEMPLATE_KOMMUNALKA_SUM[lang].format(total)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_MONTH[lang]
        telegram_send(context.bot, chat_id, text)
        return WAITING_MONTH


def process__listing_year(update: Update, context: CallbackContext):

    def compose_message(listing, year, apart, records, lang, tenant_name):
        start_year = listing.query(f"event_year < {year}")["summa"].sum()
        end_year = listing.query(f"event_year <= {year}")["summa"].sum()
        text = TEMPLATE_LISTING_ADM.format(tenant_name, apart, year, start_year) + \
            "\n".join(records) + \
            TEMPLATE_LISTING_END[lang].format(year, end_year)
        return text

    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    tenant_telegram = context.user_data["tenant_telegram"]
    chat_id = update.message.chat.id
    lang = LANGUAGE_RU
    year = date.today().year
    try:
        year = int(update.message.text)
    except ValueError:
        pass
    history = read_pgsql(("select event_year, event_text_date, apartment_number, "
        "summa::numeric, summa2::numeric, comment from vw_listing"
        f" where tenant_telegram = '{tenant_telegram}' and apartment_number={apart}"))
    listing = history.copy().query(f"event_year == {year}") if not history.empty else pd.DataFrame()
    history["summa"] = history.apply(lambda x: x["summa2"] if x["summa"] == 0 else x["summa"], axis=1)
    if not listing.empty:
        records = []
        for row in listing.itertuples():
            summa2 = ""
            if row.summa != row.summa2:
                if row.summa2 != 0:
                    temp = "–" if row.summa2 < 0 else "+"
                else:
                    temp = ""
                comment = f" {row.comment}" if row.comment != "" else ""
                summa2 = f" ({temp}{abs(row.summa2):.2f}€){comment}"
            summa = abs(row.summa)
            temp = "–" if row.summa < 0 else "+"
            records.append(TEMPLATE_LISTING_ROW.format(row.event_text_date, temp, summa, summa2))
        text = compose_message(history, year, apart, records, lang, tenant_name)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_YEAR[lang]
        telegram_send(context.bot, chat_id, text)
        return WAITING_YEAR


def process__living(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_id = update.message.from_user.username
    tenant_id = context.user_data["tenant_id"]
    full_name = context.user_data["tenant_full_name"]
    apart = context.user_data["apart"]
    price = float(update.message.text.replace(",", "."))
    query = (f"call sp_add_long_stay({tenant_id}::smallint, {apart}::smallint, {price}::money, '{staff_id}'::text);") # а где я жильца выбираю? надо sp переделать
    if exec_pgsql(query):
        start_date = date.today().strftime("%d.%m.%Y")
        end_month = (date.today().replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        days = (end_month - date.today()).days
        month_length = (end_month - date.today().replace(day=1)).days
        price = price / month_length * days
        query = ("select distinct chat_id "
            "from vw_aot_subscriber "
            "join vw_staff_aot_commands on vw_staff_aot_commands.staff_telegram = vw_aot_subscriber.staff_telegram "
            f"where {COMMAND_AOT_LIVING} = true")
        pick_recievers(context.bot, query, TEMPLATE_NEW_LONG_STAY.format(start_date, apart, full_name, price))
    else:
        telegram_send(context.bot, chat_id, TEMPLATE_COMMON_ERROR) 
    return ConversationHandler.END  


def process__out(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_id = update.message.from_user.username
    apart = context.user_data["apart"]
    tenant_name = context.user_data["tenant_name"]
    tenant_telegram = context.user_data["tenant_telegram"]
    start_date = context.user_data["living_start_date"].strftime("%d.%m.%Y")
    confirm = update.message.text.lower()
    if (confirm != TEMPLATE_YES.lower()):
        text = TEMPLATE_SEND_APART
        telegram_send(context.bot, chat_id, text)
        return WAITING_APART
    query = (
        f"call sp_process_out({apart}::smallint, '{staff_id}', 0::numeric);\n"
    )
    data = read_pgsql(query)
    if not data.empty:
        df = read_pgsql(f"select balance::numeric from vw_balance where tenant_telegram = '{tenant_telegram}'")
        balance = 0
        if not df.empty:
            balance = df["balance"].values[0]
        telegram_send(context.bot, chat_id, TEMPLATE_TENANT_DONE.format(tenant_name, apart,
            start_date, date.today().strftime("%d.%m.%Y"), data["payment_saved"].values[0], balance),
            reply_markup=ReplyKeyboardRemove())
        tenant = check_tenant(tenant_telegram)
        if (tenant is not None) and (tenant["chat_id"] != 0):
            sender = Updater(token=BOT_TOKEN, use_context=True)
            try:
                telegram_send(sender.bot, tenant["chat_id"], TEMPLATE_TENANT_GOODBYE[tenant["lang"]])
            except:
                pass
    else:
        telegram_send(context.bot, chat_id, TEMPLATE_COMMON_ERROR, 
            reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def process__price(update: Update, context: CallbackContext):
    price = None
    chat_id = update.message.chat.id
    try:
        price =  float(update.message.text.replace(",", "."))
    except ValueError:
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_SUM)
        return ConversationHandler.END
    context.user_data["price"] = price
    possible_routes = ROUTES["process__price"]
    route = context.user_data["route"]
    if route in possible_routes:
        return possible_routes[route](update, context)
    else:
        log_error(f"Route '{route}' not found in possible routes")
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_SUM, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__send_option_0(update: Update, context: CallbackContext):
    staff_chat_id = update.message.chat.id
    choice =  update.message.text
    if choice == SEND_OPTIONS[1]:
        telegram_send(context.bot, staff_chat_id, TEMPLATE_SEND_ARBITRARY_TEXT, reply_markup=ReplyKeyboardRemove())
        return WAITING_TEXT
    if choice == SEND_OPTIONS[0]:
        sender = Updater(token=BOT_TOKEN, use_context=True)
        today = date.today()
        month = today.month - 1 if today.month > 1 else 12
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
            sended = []
            for row in data.itertuples():
                if tenant != row.tenant_telegram:
                    if tenant != "":
                        try:
                            telegram_send(sender.bot, chat_id, aparment_data(apart, records, other, rent, total, lang))
                            telegram_send(sender.bot, chat_id,
                                TEMPLATE_BALANCE[lang].format(balance, TEMPLATE_MINUS if balance < 0 else TEMPLATE_PLUS) + TEMPLATE_FOOTER[lang])
                            sended.append(tenant)
                        except:
                            log_error(f"Ошибка отправки {tenant}")
                        apart = -1
                    tenant = row.tenant_telegram
                    lang = int(LANGUAGES[row.tenant_language])
                    chat_id = row.chat_id
                    balance = row.balance
                    try:
                        telegram_send(sender.bot, chat_id, TEMPLATE_HEADER[lang])
                    except:
                        log_error(f"Ошибка отправки {tenant}")
                if row.apartment_number != apart:
                    if apart != -1:
                        try:
                            telegram_send(sender.bot, chat_id, aparment_data(apart, records, other, rent, total, lang))
                        except:
                            log_error(f"Ошибка отправки {tenant}")
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
                sended.append(tenant)
            except:
                log_error(f"Ошибка отправки {tenant}")
        telegram_send(context.bot, staff_chat_id, TEMPLATE_SENDED, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def process__send_option_1(update: Update, context: CallbackContext):
    staff_chat_id = update.message.chat.id
    text =  update.message.text
    sender = Updater(token=BOT_TOKEN, use_context=True)
    sended = []
    data = read_pgsql("select tenant_telegram, chat_id from vw_actual_apartment_tenant a "
        "join bot_subscriber b ON b.tenant_id = a.tenant_id")
    if not data.empty:
        for row in data.itertuples():
            try:
                telegram_send(sender.bot, row.chat_id, text)
                sended.append(row.tenant_telegram)
            except:
                log_error(f"Ошибка отправки {row.tenant_telegram}")
    telegram_send(context.bot, staff_chat_id, TEMPLATE_SENDED, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def process__short_stay(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_id = update.message.from_user.username
    apart = context.user_data["apart"]
    first_name = context.user_data["tenant_first_name"]
    last_name = context.user_data["tenant_last_name"]
    price = context.user_data["price"]
    try:
        days = int(update.message.text)
    except ValueError:
        telegram_send(context.bot, chat_id, TEMPLATE_INPUT_ERROR)
        return WAITING_LENGTH
    query = (f"call sp_add_short_stay('{first_name}'::text, '{last_name}'::text, {apart}::smallint, "
            f"{days}::smallint, {price}::money, '{staff_id}'::text);")
    if exec_pgsql(query):
        start_date = date.today().strftime("%d.%m.%Y") 
        end_date = (date.today() + timedelta(days=days)).strftime("%d.%m.%Y")
        telegram_send(context.bot, chat_id, TEMPLATE_NEW_SHORT_STAY.format(start_date, end_date,
            apart, first_name, last_name, price * days))
    else:
        telegram_send(context.bot, chat_id, TEMPLATE_COMMON_ERROR) 
    return ConversationHandler.END  


def process__state_month(update: Update, context: CallbackContext):
    param = update.message.text.lower().replace("'", "").split(" ")
    if (len(param) == 1):
        param.append(str(date.today().year))
    chat_id = update.message.chat.id 
    month = -1
    lang = LANGUAGE_RU
    try:
        month = [x.lower() for x in MONTHS[lang]].index(param[0]) + 1
        param[0] = MONTHS[lang][month - 1]
    except ValueError:
        pass
    data = read_pgsql(("select rent_summa, utilities_summa, total_summa, payment_summa::numeric, quantity from vw_state"
        f" where year = {param[1]} and month = {month}"))
    if not data.empty:
        row = next(data.itertuples(index=False))._asdict()
        text = TEMPLATE_STATE.format(update.message.text, row["rent_summa"], row['utilities_summa'], row['total_summa'],
                                    row['payment_summa'], row['payment_summa'] - row['total_summa'], row['quantity']) #const
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_MONTH[lang]
        telegram_send(context.bot, chat_id, text)
        return WAITING_MONTH


def process__new_tenant(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    language = update.message.text.replace("'", "")
    if language not in LANGUAGES:
        telegram_send(context.bot, chat_id, TEMPLATE_TENANT_LANG_ERROR, 
            reply_markup=ReplyKeyboardMarkup([[n for n in LANGUAGES]], resize_keyboard=True))
        return WAITING_TENANT_LANGUAGE
    first_name = context.user_data["tenant_first_name"].replace("'", "")
    last_name = context.user_data["tenant_last_name"].replace("'", "")
    telegram = context.user_data["tenant_telegram"].replace("'", "")
    query = f"call sp_add_tenant('{first_name}', '{last_name}', '{telegram}', '{language}')"
    if exec_pgsql(query):
        text = TEMPLATE_TENANT_ADDED.format(first_name, last_name)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        text = TEMPLATE_TENANT_WELCOME[LANGUAGES[language]].format(first_name)
        telegram_send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
    else:
        telegram_send(context.bot, chat_id, TEMPLATE_COMMON_ERROR, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def process__tenant(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    tenant_name = update.message.text.replace("'", "''")
    query = ("select living_id, tenant_telegram from vw_living "
        f"where tenant_full_name = '{tenant_name}' and apartment_number={apart} "
        "order by living_start_date desc limit 1")
    data = read_pgsql(query)
    if data.empty:
        telegram_send(context.bot, chat_id, f"{TEMPLATE_ERROR_IN_APART}\n{TEMPLATE_SEND_TENANT.format(apart)}")
        return WAITING_TENANT
    context.user_data["tenant_name"] = tenant_name
    context.user_data["living_id"] = data["living_id"].values[0]
    context.user_data["tenant_telegram"] = data["tenant_telegram"].values[0]
    possible_routes = ROUTES["process__tenant"]
    route = context.user_data["route"]
    if route in possible_routes:
        return possible_routes[route](update, context)
    else:
        log_error(f"Route '{route}' not found in possible routes")
        telegram_send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def process__transfer_money(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    staff_id = update.message.from_user.username
    from_cashbox = context.user_data["from_cashbox"]
    to_cashbox = context.user_data["to_cashbox"]
    summa = context.user_data["summa"]
    if exec_pgsql((f"call sp_add_transfer_order('{staff_id}', {from_cashbox['cashbox_id']}::smallint, "
        f"{to_cashbox['cashbox_id']}::smallint, {summa}::money);")): 
        query = ("select distinct chat_id "
            "from vw_aot_subscriber "
            "join vw_staff_cashbox on vw_staff_cashbox.staff_id = vw_aot_subscriber.staff_id "
            f"where cashbox_id in ({to_cashbox['cashbox_id']}, {from_cashbox['cashbox_id']}) AND can_see_balance")
        pick_recievers(context.bot, query, TEMPLATE_TRANSFER_COMPLETED.format(summa, from_cashbox["cashbox_name"], to_cashbox["cashbox_name"]))
    else:
        text = TEMPLATE_TRANSFER_GENERAL_ERROR
        telegram_send(context.bot, chat_id, text)

    return ConversationHandler.END

def error_handler(update: object, context: CallbackContext) -> None:
    log_error(context.error)
    traceback.print_tb(context.error.__traceback__)


def main():
    global updater, ROUTES

    updater = Updater(token=AOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # dispatcher.add_handler(CommandHandler(COMMAND_EXIT, command_exit), 0)

    dispatcher.add_handler(CommandHandler(COMMAND_START, command_start), 1)

    dispatcher.add_handler(ConversationHandler(
        name="add",
        entry_points=[
            CommandHandler(COMMAND_AOT_ADD, command_add)
        ],
        states={
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & (~Filters.command), process__apart),
                MessageHandler(Filters.text & ~Filters.command, command_add)
            ],
            WAITING_TENANT: [
                MessageHandler(Filters.text & ~Filters.command, process__tenant)
            ],
            WAITING_SUM: [
                MessageHandler(Filters.text & ~Filters.command, process__add_sum),
            ],
            WAITING_CASHBOX: [
                MessageHandler(Filters.text & ~Filters.command, process__add_cashbox),
            ],
            WAITING_CONFIRM_SUM: [
                MessageHandler(Filters.text & ~Filters.command, process__add_confirm_sum),
            ]
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 2)

    dispatcher.add_handler(ConversationHandler(
        name="upload",
        entry_points=[
            CommandHandler(COMMAND_AOT_UPLOAD, command_upload)
        ],
        states={
            WAITING_SERVICE: [
                MessageHandler(Filters.regex(
                    f"^({'|'.join([TEMPLATE_SERVICES[i][LANGUAGE_RU] for i in UTILITES_SERVICE_IDS])})$") & \
                    ~Filters.command, conversation__upload_select_service
                ),
                MessageHandler(Filters.text & ~Filters.command, command_upload)
            ],
            WAITING_FILE: [
                MessageHandler(Filters.document, process__file),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 3)

    dispatcher.add_handler(ConversationHandler(
        name="balance",
        entry_points=[
            CommandHandler(COMMAND_AOT_BALANCE, command_balance)
        ],
        states={
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
                MessageHandler(Filters.text & ~Filters.command, command_balance)
            ],
            WAITING_TENANT: [
                MessageHandler(Filters.text & ~Filters.command, process__tenant),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 4)

    dispatcher.add_handler(ConversationHandler(
        name="info",
        entry_points=[
            CommandHandler(COMMAND_AOT_INFO, command_info)
        ],
        states={
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
                MessageHandler(Filters.text & ~Filters.command, command_info)
            ],
            WAITING_TENANT: [
                MessageHandler(Filters.text & ~Filters.command, process__tenant),
            ],
            WAITING_MONTH: [
                MessageHandler(Filters.text & ~Filters.command, process__info_month),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 5)

    dispatcher.add_handler(ConversationHandler(
        name="listing",
        entry_points=[
            CommandHandler(COMMAND_AOT_LISTING, command_listing)
        ],
        states={
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
                MessageHandler(Filters.text & ~Filters.command, command_listing)
            ],
            WAITING_TENANT: [
                MessageHandler(Filters.text & ~Filters.command, process__tenant),
            ],
            WAITING_YEAR: [
                MessageHandler(Filters.text & ~Filters.command, process__listing_year),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 6)

    dispatcher.add_handler(MessageHandler(Filters.command,
        lambda update, context: telegram_send(context.bot, update.message.chat.id,
            "Неподдерживаемая команда", ret_val=ConversationHandler.END)
    ), 7)

    dispatcher.add_handler(ConversationHandler(
        name="transfer",
        entry_points=[
            CommandHandler(COMMAND_AOT_TRANSFER, command_transfer)
        ],
        states={
            WAITING_CASHBOX: [
                MessageHandler(Filters.regex(r"^.+\s[>]\s.+$") & ~Filters.command, conversation__transfer_cashboxes),
            ],
            WAITING_SUM: [
                MessageHandler(Filters.regex(r"^\d+([.,]+\d{1,2})*$") & ~Filters.command, conversation__transfer_sum),
            ]
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 8)

    dispatcher.add_handler(ConversationHandler(
        name="state",
        entry_points=[
            CommandHandler(COMMAND_AOT_STATE, command_state)
        ],
        states={
            WAITING_MONTH: [
                MessageHandler(Filters.text & ~Filters.command, process__state_month),
            ],
        },
        fallbacks=[
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 12)

    dispatcher.add_handler(ConversationHandler(
        name="debtors",
        entry_points=[
            CommandHandler(COMMAND_AOT_DEBTORS, command_debtors)
        ],
        states={},
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 13)

    dispatcher.add_handler(ConversationHandler(
        name="debtors_no_balance",
        entry_points=[
            CommandHandler(COMMAND_AOT_DEBTORS_NO_BALANCE, command_debtors_no_balance)
        ],
        states={},
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 15)

    dispatcher.add_handler(ConversationHandler(
        name="free_apart",
        entry_points=[
            CommandHandler(COMMAND_AOT_FREE_APART, command_free_apart)
        ],
        states={},
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 14)

    dispatcher.add_handler(ConversationHandler(
        name="tenant",
        entry_points=[
            CommandHandler(COMMAND_AOT_TENANT, command_new_tenant)
        ],
        states={
            WAITING_CONTACT: [
                MessageHandler(Filters.contact & ~Filters.command, conversation__new_tenant_first_name),
                MessageHandler(Filters.text & ~Filters.command, command_new_tenant)
            ],
            WAITING_TENANT_NAME: [
                MessageHandler(Filters.text & ~Filters.command, conversation__new_tenant_last_name),
            ],
            WAITING_TENANT_LASTNAME: [
                MessageHandler(Filters.text & ~Filters.command, conversation__new_tenant_language),
            ],
            WAITING_TENANT_LANGUAGE: [
                MessageHandler(Filters.text & ~Filters.command, process__new_tenant),
            ]
        },
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 16)

    dispatcher.add_handler(ConversationHandler(
        name="living",
        entry_points=[
            CommandHandler(COMMAND_AOT_LIVING, command_living)
        ],
        states={
            WAITING_CONTACT: [
                MessageHandler(Filters.contact & ~Filters.command, conversation__select_tenant),
                #MessageHandler(Filters.text & ~Filters.command, command_new_tenant)
            ],
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
            ],
            WAITING_PRICE: [
                MessageHandler(Filters.regex(r"^\d+$") & ~Filters.command, process__price),
            ],
        },
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 17)

    dispatcher.add_handler(ConversationHandler(
        name="short_stay",
        entry_points=[
            CommandHandler(COMMAND_AOT_SHORT_STAY, command_short_stay)
        ],
        states={
            WAITING_TENANT_NAME: [
                MessageHandler(Filters.text & ~Filters.command, conversation__short_stay_last_name),
            ],
            WAITING_TENANT_LASTNAME: [
                MessageHandler(Filters.text & ~Filters.command, conversation__short_stay_apart),
            ],
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
            ],
            WAITING_PRICE: [
                MessageHandler(Filters.regex(r"^\d+([.,]+\d{1,2})*$") & ~Filters.command, process__price),
            ],
            WAITING_LENGTH: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-9][0-9]|[1-2][0-9][0-9])$") & ~Filters.command, process__short_stay),
            ]
        },
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 18)

    dispatcher.add_handler(ConversationHandler(
        name="out",
        entry_points=[
            CommandHandler(COMMAND_AOT_OUT, command_out)
        ],
        states={
            WAITING_APART: [
                MessageHandler(Filters.regex(r"^([1-9]|[1-5][0-9]|6[0-6])$") & ~Filters.command, process__apart),
                MessageHandler(Filters.text & ~Filters.command, command_out)
            ],
            WAITING_YES_NO: [
                MessageHandler(Filters.text & ~Filters.command, process__out),
            ]
        },
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 19)

    dispatcher.add_handler(ConversationHandler(
        name="send",
        entry_points=[
            CommandHandler(COMMAND_AOT_SEND, command_send)
        ],
        states={
            WAITING_CHOICE: [
                MessageHandler(Filters.text & ~Filters.command, process__send_option_0),
            ],
            WAITING_TEXT: [
                MessageHandler(Filters.text & ~Filters.command, process__send_option_1),
            ]
        },
        fallbacks=[ 
            MessageHandler(Filters.command, command_exit)
        ],
        conversation_timeout=60
        ), 20)

    ROUTES = {
        "process__apart": {
            COMMAND_AOT_ADD: conversation__list_tenants,
            COMMAND_AOT_BALANCE: conversation__list_tenants,
            COMMAND_AOT_INFO: conversation__list_tenants,
            COMMAND_AOT_LISTING: conversation__list_tenants,
            COMMAND_AOT_OUT: conversation__out,
            COMMAND_AOT_SHORT_STAY: process__check_free_apart,
            COMMAND_AOT_LIVING: process__check_free_apart,
        },
        "process__tenant": {
            COMMAND_AOT_ADD: conversation__add_sum,
            COMMAND_AOT_BALANCE: process__balance,
            COMMAND_AOT_INFO: conversation__info_month,
            COMMAND_AOT_LISTING: conversation__listing_year,
        },
        "process__price": {
            COMMAND_AOT_SHORT_STAY: conversation__short_stay_length,
            COMMAND_AOT_LIVING: process__living,
        }
    }

    dispatcher.add_error_handler(error_handler)

    print("Akacia aot started")

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
