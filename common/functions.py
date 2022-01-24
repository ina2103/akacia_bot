from datetime import datetime
from functools import lru_cache
import pandas as pd
import psycopg2
from typing import Dict, List, Union

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

from common import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, LANGUAGES


def log_error(msg: str):
    '''
    Logs an error message to the console.

    :param msg: str
    :type msg: str
    :return: None
    '''
    logging.log(logging.ERROR, msg)


def cachetime(minutes: int = 1):

    @lru_cache(10)
    def executor(f, time, name):
        return f()

    def decorator(f):
        def wrapper():
            tp = datetime.now().timetuple()
            m = (tp.tm_min + tp.tm_hour * 60) / (minutes if minutes > 0 and minutes < 61 else 1)
            v = executor(f, m, f.__name__)
            return v
        return wrapper

    return decorator


def connect_pgsql():
    '''
    It connects to a PostgreSQL database using the psycopg2 library.

    :return: A connection object.
    '''
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def read_pgsql(query: str) -> pd.DataFrame:
    '''
    It connects to the PostgreSQL database, executes the query, and returns the result as a Pandas
    DataFrame.

    :param query: str
    :return: A DataFrame
    '''
    with connect_pgsql() as DB:
        try:
            df = pd.read_sql(query, con=DB)
            DB.commit()
            return df
        except Exception as e:
            log_error(f'Error executing query "{query}": {str(e)}')
        return pd.DataFrame()


def exec_pgsql(query: str) -> bool:
    '''
    It connects to the PostgreSQL database, executes the query, and commits the changes.

    :param query: str
    :return: result as boolean
    '''
    with connect_pgsql() as DB:
        try:
            with DB.cursor() as cursor:
                cursor.execute(query)
                DB.commit()
            return True
        except Exception as e:
            log_error(f'Error executing query "{query}": {str(e)}')
        return False


@cachetime(5)
def read_tenants() -> pd.DataFrame:
    '''
    It reads the tenants table from the database and returns it as a pandas dataframe.

    :return: A DataFrame with all the tenants.
    '''
    try:
        tenants = read_pgsql(("select t.*, COALESCE(b.chat_id, 0::bigint) as chat_id from vw_tenant t "
            "LEFT OUTER JOIN bot_subscriber b ON b.tenant_id = t.tenant_id"))
        return tenants
    except Exception as e:
        log_error(f'Error executing query "select * from vw_tenant": {str(e)}')
    return pd.DataFrame()


@cachetime(5)
def read_staff() -> pd.DataFrame:
    '''
    It reads the staff table from the database and returns it as a pandas dataframe.

    :return: A DataFrame
    '''
    try:
        staff = read_pgsql("select * from vw_staff_aot_commands")
        return staff.fillna(False)
    except Exception as e:
        log_error(f'Error executing query "select * from vw_staff_aot_commands": {str(e)}')
    return pd.DataFrame()


def check_tenant(tenant_telegram: str) -> Union[Dict, None]:
    '''
    Given a tenant's telegram, return a dictionary with the tenant's id, language and chat_id.

    :param tenant_telegram: str
    :return: A dictionary with the following keys:
        id: The id of the tenant
        lang: The language of the tenant
        chat_id: The chat id of the tenant
    '''
    try:
        tenants = read_tenants()
        if not tenants.empty:
            tenants = tenants.query(f"tenant_telegram == '{tenant_telegram}'").reset_index()
            if not tenants.empty:
                row = tenants.loc[0][["tenant_id", "tenant_language", "chat_id"]].values
                return dict(id=int(row[0]), lang=int(LANGUAGES[str(row[1])]), chat_id=str(row[2]))
    except:
        log_error("Error check tenant")
    return None


def check_staff(staff_telegram: str, command: str) -> Union[Dict, None]:
    try:
        staff = read_staff()
        if not staff.empty:
            staff = staff.query(f"staff_telegram == '{staff_telegram}'")
            if not staff.empty:
                return staff[command].values[0] if command in staff.columns else True
    except:
        log_error("Error check staff")
    return False


def select_allowed_cashboxes(staff_telegram: str) -> List[Dict]:
    query = f"select * from vw_staff_cashbox where staff_telegram='{staff_telegram}' order by cashbox_name"
    cashboxes = read_pgsql(query)
    return [c._asdict() for c in cashboxes.itertuples(index=False)]


def telegram_create_keyboard(buttons: List) -> List:
    '''
    Create a list of lists of buttons.

    :param buttons: List of strings
    :return: Buttons separated by 3 in row
    '''
    result = []
    for i in range(int(len(buttons) / 3) + 1):
        if (len(buttons) <= 3):
            result.append(buttons)
            break
        result.append(buttons[:3])
        buttons = buttons[3:]
    return result


def telegram_send(bot, chat_id, text, reply_markup=None, ret_val=None):
    '''
    Send a message to a chat.

    :param bot: The bot object
    :param chat_id: The chat id of the user to send the message to
    :param text: The text of the message to be sent
    :param reply_markup: This is the keyboard that will be shown to the user
    :param ret_val: If you want to return a value from the function, you can do so by setting ret_val to
    the value you want to return
    :return: The message object.
    '''
    return bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=reply_markup) if ret_val is None else ret_val
