from typing import List
from common.functions import read_pgsql

COMMAND_BOT_BALANCE = "balance"
COMMAND_BOT_INFO = "info"
COMMAND_BOT_LISTING = "listing"

COMMAND_EXIT = "exit"
COMMAND_START = "start"
COMMAND_STOP = "stop"

def __get_command_acronyms() -> List:
    _ = read_pgsql("select * from aot_command")
    if not _.empty:
        return _.sort_values(by=["aot_command_id"])["aot_command_acronym"].values.tolist()
    return [f"command{i}" for i in range(10)]


COMMAND_AOT_ADD, COMMAND_AOT_DRAW, COMMAND_AOT_CASHBOX, COMMAND_AOT_COLLECTION, \
COMMAND_AOT_TRANSFER, COMMAND_AOT_PAYMENTS, COMMAND_AOT_BALANCE, COMMAND_AOT_INFO, \
COMMAND_AOT_BUDGET, COMMAND_AOT_UPLOAD, COMMAND_AOT_LISTING, COMMAND_AOT_STATE, \
COMMAND_AOT_DEBTORS, COMMAND_AOT_FREE_APART = __get_command_acronyms()

