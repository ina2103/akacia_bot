#!/home/ec2-user/bot/bin/python3

import os
os.chdir("/home/ec2-user/akacia_bot")

from common.constants import *
from common.functions import *

if exec_pgsql("call sp_add_monthly_rent();"):
    print("Monthly rent was added")
else:
    print("Error in adding monthly rent")