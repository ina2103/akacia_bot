#!/home/ec2-user/bot/bin/python3

import os
from telegram.ext import Updater
os.chdir("/home/ec2-user/akacia_bot")

from common import *
from common.functions import *

def telegram_check(data, token):
    for user in data.itertuples():
        updater = Updater(token=token, use_context=True)
        user_data = updater.bot.get_chat(user.chat_id)
        if user_data.username is not None and user_data.username != "":
            if user_data.username != user.tenant_telegram:
                exec_pgsql(f"call sp_update_tenant_telegram ({user.tenant_id}::smallint, '{user_data.username}'::text);")
                print(f"Username был изменен с {user.tenant_telegram} на {user_data.username} для id = {user.tenant_id}")

data = read_pgsql("select tenant_id, tenant_telegram, chat_id from vw_bot_subscriber")
telegram_check(data, BOT_TOKEN)

data = read_pgsql("select staff_id as tenant_id, staff_telegram as tenant_telegram, chat_id from vw_aot_subscriber")
telegram_check(data, AOT_TOKEN)