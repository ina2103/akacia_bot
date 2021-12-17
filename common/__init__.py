import yaml

with open("./settings.yml") as file:
    settings = yaml.full_load(file)

BOT_TOKEN = settings["telegram"]["bot_token"]
AOT_TOKEN = settings["telegram"]["aot_token"]

DB_HOST = settings["db"]["db_host"]
DB_NAME = settings["db"]["db_name"]
DB_PORT = settings["db"]["db_port"]
DB_USER = settings["db"]["db_user"]
DB_PASSWORD = settings["db"]["db_password"]

LANGUAGE_RU: int = 0
LANGUAGE_SR: int = 1
LANGUAGE_EN: int = 2

LANGUAGES = { "RU": LANGUAGE_RU, "SR": LANGUAGE_SR, "EN": LANGUAGE_EN }
