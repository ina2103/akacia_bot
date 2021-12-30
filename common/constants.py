from common.commands import *
from common import LANGUAGE_EN, LANGUAGE_RU, LANGUAGE_SR


SUM_REGEX = (r"^(?P<payment_recieved>(0|[1-9][0-9]*)([.][0-9]+)*)(\s+(?P<payment_saved>[-]|(0|[1-9][0-9]*)([.][0-9]+)*)*"
            r"(\s+?(?P<comment>.*))*)*$")

WAITING_MONTH = 666
WAITING_YEAR = 667

WAITING_APART = 333
WAITING_TENANT = 334
WAITING_SUM = 335
WAITING_CONFIRM_SUM = 336
WAITING_CLAUSE = 337
WAITING_CASHBOX = 338
WAITING_SERVICE = 339
WAITING_FILE = 340
WAITING_YES_NO = 341

MONTHS = {
    LANGUAGE_RU: ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
    LANGUAGE_SR: ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"],
    LANGUAGE_EN: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
}

TEMPLATE_WIP = (
    "Бот на профилактике — приходите завтра.\n\n"
    "Radovi u toku, dođite sutra.\n\n"
    "Work in progress, please come tomorrow."
)

TEMPLATE_NOT_FOUND = (
    "Тебя нет среди жителей Акации. Спроси @akaciom почему.\n\n"
    "Nismo našli vas u spisku stanara Akaciji. Pitajte @akaciom zašto.\n\n"
    "You aren't found in list of Akacia apartments' renters. Please, ask @akaciom to add you."
)

TEMPLATE_PAYMENTS_NOT_FOUND = {
    LANGUAGE_RU: "Нет оплат за <b>{0}</b> год. А должны быть? Спроси @akaciom где твои оплаты.\n\n",
    LANGUAGE_SR: "Nemamo računa za <b>{0}</b> godinu. Ako mislite na grešku pa pitajte @akaciom.\n\n",
    LANGUAGE_EN: "Payments for <b>{0}</b> are not found. If you aren't ok with it, please, ask @akaciom what happend."
}

TEMPLATE_BILLS_NOT_FOUND = {
    LANGUAGE_RU: "Нет начислений. А должны быть? Спроси @akaciom где твои начисления.\n\n",
    LANGUAGE_SR: "Nema računa. Ako mislite na grešku pa kontaktirate administraciju.\n\n",
    LANGUAGE_EN: "Bills for <b>{0}</b> are not found. If you aren't ok with it, please, ask @akaciom what happend."
}

TEMPLATE_HEADER = {
    LANGUAGE_RU: "Тук-тук! Настал день арендной платы! :)\n\n",
    LANGUAGE_SR: "Kuc-kuc! Došao je dan naplate! :)\n\n",
    LANGUAGE_EN: "Knock-knock! It's a rent payment day! :)\n\n"
}

TEMPLATE_TOTAL = {
    LANGUAGE_RU: "Квартира <b>{}</b>:\n— Аренда <b>{}</b> <b>{:.2f}€</b>\n",
    LANGUAGE_SR: "Po stanu <b>{}</b> uračunato:\n— za <b>{}</b> boravište <b>{:.2f}€</b>\n",
    LANGUAGE_EN: "For apartment <b>{}</b> bills are:\n— <b>{}</b>'s rent <b>{:.2f}€</b>\n"
}

TEMPLATE_OTHER_SERVICES = {
    LANGUAGE_RU: "Другие услуги:\n",
    LANGUAGE_SR: "Ostale usluge:\n",
    LANGUAGE_EN: "Other services:\n"
}

TEMPLATE_FOOTER = {
    LANGUAGE_RU: "\n\nСпасибо, что живете в Акации! ❤️",
    LANGUAGE_SR: "\n\nHvala vam sto živite u Akaciji! ❤️",
    LANGUAGE_EN: "\n\nThank you for living at Akacia apartments! ❤️"
}

TEMPLATE_MINUS = "💔"
TEMPLATE_PLUS = "❤️"

RENT_SERVICE_ID = 4
UTILITES_SERVICE_IDS = [1, 2, 3]

TEMPLATE_SERVICES = [
    {},
    {
        LANGUAGE_RU: "вода",
        LANGUAGE_SR: "voda",
        LANGUAGE_EN: "water"
    },
    {
        LANGUAGE_RU: "электричество",
        LANGUAGE_SR: "struja",
        LANGUAGE_EN: "electricity"
    },
    {
        LANGUAGE_RU: "мусор",
        LANGUAGE_SR: "odvoz smeća",
        LANGUAGE_EN: "garbage disposal"
    },
    {
        LANGUAGE_RU: "аренда",
        LANGUAGE_SR: "boravište",
        LANGUAGE_EN: "rent"
    },
    {
        LANGUAGE_RU: "регистрация",
        LANGUAGE_SR: "registracija",
        LANGUAGE_EN: "registration"
    },
]

TEMPLATE_INFO = {
    LANGUAGE_RU: ("По квартире <b>{}</b> за <b>{}</b> начислено:\n"
        f"— {TEMPLATE_SERVICES[RENT_SERVICE_ID][LANGUAGE_RU]}"
        " <b>{:.2f}€</b>\n"),
    LANGUAGE_SR: ("Po stanu <b>{}</b> za <b>{}</b> uračunato:\n"
        f"— {TEMPLATE_SERVICES[RENT_SERVICE_ID][LANGUAGE_SR]}"
        " <b>{:.2f}€</b>\n"),
    LANGUAGE_EN: ("<b>{1}</b> bills for apartment <b>{0}</b> are:\n"
        f"— {TEMPLATE_SERVICES[RENT_SERVICE_ID][LANGUAGE_EN]}"
        " <b>{2:.2f}€</b>\n")
}

TEMPLATE_KOMMUNALKA_MONTH = {
    LANGUAGE_RU: "— Ресурсы <b>{}</b>:\n",
    LANGUAGE_SR: "— Komunalije za <b>{}</b>:\n",
    LANGUAGE_EN: "— Municipal services for <b>{}</b>:\n"
}

TEMPLATE_KOMMUNALKA_ROW = "— {} <b>{:.2f}€</b>\n"

TEMPLATE_KOMMUNALKA_SUM = {
    LANGUAGE_RU: "Итого: <b>{:.2f}€</b>\n\n",
    LANGUAGE_SR: "Ukupno: <b>{:.2f}€</b>\n\n",
    LANGUAGE_EN: "Total: <b>{:.2f}€</b>\n\n"
}

TEMPLATE_DEBT = {
    LANGUAGE_RU: "минус",
    LANGUAGE_SR: "dug",
    LANGUAGE_EN: "debt"
}

TEMPLATE_PREPAID = {
    LANGUAGE_RU: "плюс",
    LANGUAGE_SR: "bilans",
    LANGUAGE_EN: "advance payment"
}

TEMPLATE_BALANCE = {
    LANGUAGE_RU: "Твой баланс <b>{:.2f}€</b> {}",
    LANGUAGE_SR: "Trenutni bilans je <b>{:.2f}€</b> {}",
    LANGUAGE_EN: "The current balance is <b>{:.2f}€</b> {}"
}

TEMPLATE_PAYMENTS = {
    LANGUAGE_RU: "За <b>{}</b> год по квартире <b>{}</b> поступило оплат:\n\n",
    LANGUAGE_SR: "Za <b>{}</b> godinu po stanu <b>{}</b> ima računa:\n\n",
    LANGUAGE_EN: "These payments were received in <b>{}</b> for apartment <b>{}</b>:\n\n",
}

TEMPLATE_START = {
    LANGUAGE_RU: "Рад приветствовать тебя в Акации!\n\nТеперь ты часть нашего комьюнити, так что давай знакомиться ближе. Вот что тебе нужно знать о нас:\n\nМы любим своих соседей, не стесняемся просить их о помощи и, по возможности, помогаем сами.\n\nВсе мы разные, но всегда готовы выслушать и понять друг друга, ведь случайных людей среди нас нет. Короч, don’t be negative, just be positive!\n\nНаш стаф всегда придет на помощь, но в собственном ритме, и замутит то, что поможет жить вам 😉\n\nАкация стала твоим домом, береги его! ❤️ И подпишись на нас в Инстаграм: https://instagram.com/akacia_apart.\n\nА чтобы остановить подписку просто отправь мне /stop",
    LANGUAGE_SR: "Vi ste potpisani na obaveštenje od Akaciji. Za prekid pošaljite poruku /stop",
    LANGUAGE_EN: "You are subscribed to the message list from the Akacia apartments. Send /stop to stop your subscription. Feel free to follow us on Instagram: https://instagram.com/akacia_apart"
}

TEMPLATE_STOP = {
    LANGUAGE_RU: "Хорошо, не буду тебя отвлекать.\nЕсли снова понадоблюсь, просто напиши мне /start",
    LANGUAGE_SR: "Prekinuli ste obaveštenje od Akaciji. Za potpisku pošaljite poruku /start",
    LANGUAGE_EN: "You are unsubscribed from the Akacia apartments' message list. Send /start to start your subscription."
}

TEMPLATE_COMMAND_EXIT = {
    LANGUAGE_RU: f" или отправьте /{COMMAND_EXIT}.",
    LANGUAGE_SR: f" ili poslati /{COMMAND_EXIT}.",
    LANGUAGE_EN: f" or send /{COMMAND_EXIT}."
}

TEMPLATE_SELECT_MONTH = {
    LANGUAGE_RU: "Выберите месяц" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU],
    LANGUAGE_SR: "Izaberite mesec koji je potreban za izvod računa" + TEMPLATE_COMMAND_EXIT[LANGUAGE_SR],
    LANGUAGE_EN: "Send the month for which you want to get information on bills" + TEMPLATE_COMMAND_EXIT[LANGUAGE_EN]
}

TEMPLATE_SELECT_AVAILABLE_MONTH = {
    LANGUAGE_RU: "Выберите месяц" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU],
    LANGUAGE_SR: "Izaberite dostupan mesec" + TEMPLATE_COMMAND_EXIT[LANGUAGE_SR],
    LANGUAGE_EN: "Select a month with available data" + TEMPLATE_COMMAND_EXIT[LANGUAGE_EN]
}

TEMPLATE_SELECT_YEAR = {
    LANGUAGE_RU: "Выберите год" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU],
    LANGUAGE_SR: "Izaberite godinu koji je potreban za izvod računa" + TEMPLATE_COMMAND_EXIT[LANGUAGE_SR],
    LANGUAGE_EN: "Send the year for which you want to get information" + TEMPLATE_COMMAND_EXIT[LANGUAGE_EN]
}

TEMPLATE_SELECT_AVAILABLE_YEAR = {
    LANGUAGE_RU: "Выберите доступный год" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU],
    LANGUAGE_SR: "Izaberite dostupan godinu" + TEMPLATE_COMMAND_EXIT[LANGUAGE_SR],
    LANGUAGE_EN: "Select a year with available data" + TEMPLATE_COMMAND_EXIT[LANGUAGE_EN]
}

TEMPLATE_LISTING_BILL = TEMPLATE_MINUS + "<pre> {} <b>–{:.2f}€</b></pre>"
TEMPLATE_LISTING_PAYMENT = TEMPLATE_PLUS + "<pre> {} <b>+{:.2f}€</b></pre>"

TEMPLATE_LISTING_START = {
    LANGUAGE_RU: "Твой баланс в начале {} года <b>{:.2f}€</b>.\n\n",
    LANGUAGE_SR: "U pocetku {}. godine bilans je <b>{:.2f}€</b>.\n\n",
    LANGUAGE_EN: "On January 1st, {} the balance is <b>{:.2f}€</b>.\n\n"
}

TEMPLATE_LISTING_END = {
    LANGUAGE_RU: "\n\nПо итогам {} года <b>{:.2f}€</b>.",
    LANGUAGE_SR: "\n\nNa kraju {}. godine bilans je <b>{:.2f}€</b>.",
    LANGUAGE_EN: "\n\nOn end of {} the balance is <b>{:.2f}€</b>."
}

TEMPLATE_EXIT_CONVERSATION = {
    LANGUAGE_RU: "Вы вышли из диалога.",
    LANGUAGE_SR: "Izašao si iz dijaloga.",
    LANGUAGE_EN: "You exited from dialog."
}
TEMPLATE_TENANT_GOODBYE = {
    LANGUAGE_RU: "Спасибо, что жили в Акации. Ждем снова ❤️",
    LANGUAGE_SR: "Hvala vam što ste ostali sa nama ❤️",
    LANGUAGE_EN: "Thank you for staying with us. Hope to see you again ❤️"
}

TEMPLATE_BALANCE_ADM = "Баланс пользователя <b>{}</b> по квартире <b>{}</b>: <b>{}€</b>"
TEMPLATE_BALANCE_ADM_TOTAL = "\nОбщий баланс: <b>{}€</b>"
TEMPLATE_INFO_ADM = "Пользователю <b>{}</b> по квартире <b>{}</b> за <b>{}</b> начислено:\n— аренда <b>{:.2f}€</b>\n"
TEMPLATE_LISTING_ADM = "Баланс пользователя <b>{}</b> по квартире <b>{}</b> в начале {} года <b>{:.2f}€</b>.\n\n"
TEMPLATE_LISTING_ROW = "<pre> {} <b>{}{:.2f}€</b>{}</pre>"
TEMPLATE_YES = "Да"
TEMPLATE_NO = "Нет. НЕТ! Срочная отмена!!1"
TEMPLATE_MANAGER_NOT_FOUND = "https://www.youtube.com/watch?v=7OBx-YwPl8g"
TEMPLATE_MANAGER_NO_PERMISSION = "У вас нет прав на выполнение этой команды."
TEMPLATE_MANAGER_FOUND = f"Отправьте команду /{COMMAND_AOT_ADD} для добавления новой записи о внесении денег."
TEMPLATE_ERROR_IN_APART = "Неверный номер квартиры, имя жильца или нет записей о проживании."
TEMPLATE_SEND_APART = "Отправьте номер квартиры" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_SEND_DATE_IN = "Отправьте дату заезда в квартиру <b>{}</b>"
TEMPLATE_SEND_DATE_OUT = "Отправьте дату выезда <b>{}</b> из квартиры <b>{}</b>"
TEMPLATE_SEND_TENANT = "Отправьте имя арендатора из квартиры <b>{}</b>" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_SEND_SUM = ("Отправьте сумму, принятую от <b>{}</b> из квартиры <b>{}</b> (целое число без пробелов)"
    f"{TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]}")
TEMPLATE_ERROR_SUM = "Неверная сумма."
TEMPLATE_CONFIRM_SUM = "Внести <b>{:.2f}€</b> (как <b>{:.2f}€</b>) от <b>{}</b> в счёт оплаты квартиры <b>{}</b>?"
TEMPLATE_DATA_SAVED = "Данные об оплате <b>{:.2f}€</b> (как <b>{:.2f}€</b>) от <b>{}</b> по квартире <b>{}</b> сохранены."
TEMPLATE_DATA_SENDED = "Пользователю <b>{}</b> было отправлено об этом сообщение."
TEMPLATE_PAYMENTS_BY_RENTER = "От <b>{}</b> по квартире <b>{}</b> поступило оплат:\n\n"
TEMPLATE_PAYMENT_ACCEPTED = {
    LANGUAGE_RU: "Получил <b>{:.2f}€</b> за квартиру <b>{}</b>! ❤️",
    LANGUAGE_SR: "Iznos od <b>{:.2f}€</b> za stan <b>{}</b> biće uplaćen na vaš račun u toku dana. Zahvaljujemo na redovnoj uplati!",
    LANGUAGE_EN: "Payment <b>{:.2f}€</b> for apartment <b>{}</b> was placed on your account. Thank you for paying in time!"
}
TEMPLATE_BUDGET = "Доступный бюджет по статьям на <b>{}</b>:\n{}"
TEMPLATE_BUDGET_ITEM = "• {} — <b>{}€</b>"
TEMPLATE_NO_CLAUSES = "Не найдено доступных вам статей бюджета."
TEMPLATE_SELECT_CLAUSE = "Выберите подстатью бюджета, с которой необходимо запросить средства" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_CLAUSE_NOT_FOUND = "Не найдена подстатья <b>{}</b>, либо нет доступного бюджета на текущий месяц."
TEMPLATE_DRAW_SUM = "По статье <b>{}</b> на <b>{}</b> осталось <b>{}€</b>.\nВведите запрашиваеммую сумму" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_DRAW_RECIEVED = "Заявка на сумму <b>{}€</b> по статье <b>{}</b> принята на рассмотрение."
TEMPLATE_DRAW_CONFIRMED = "Заявка на сумму <b>{}€</b> по статье <b>{}</b> от пользователя <b>{}</b> одобрена.\n<i>Исполнитель: {}</i>"
TEMPLATE_DRAW_DECLINED = "Заявка на сумму <b>{}€</b> по статье <b>{}</b> от пользователя <b>{}</b> отклонена.\n<i>Исполнитель: {}</i>"
TEMPLATE_DRAW_REQUEST = "Получена заявка на сумму <b>{}€</b> по статье <b>{}</b> от пользователя <b>{}</b>"
TEMPLATE_DRAW_NOT_FOUND = "Заявка не найдена"
TEMPLATE_DRAW_BUTTON_OK = "Принять"
TEMPLATE_DRAW_BUTTON_NO = "Отклонить"
TEMPLATE_CASHBOX_BALANCE = "Остатки по кассам:\n{}"
TEMPLATE_CASHBOX_BALANCE_ITEM = "• {} — <b>{:.2f}€</b>"
TEMPLATE_NO_CASHBOXES = "Не найдены кассы."
TEMPLATE_SELECT_CASHBOX = "Выберите кассу для внесения" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_SELECT_CASHBOXES = "Выберите кассы" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU]
TEMPLATE_SUM_TO_TRANSFER = "Введите сумму для перевода из кассы <b>{}</b> в кассу <b>{}</b>" + TEMPLATE_COMMAND_EXIT[LANGUAGE_RU] + \
    " Текущий остаток в кассе <b>{}</b> — <b>{}€</b>."
TEMPLATE_TRANSFER_COMPLETED = "Совершён перевод:\n<b>{}€</b> переведены из кассы <b>{}</b> в кассу <b>{}</b>."
TEMPLATE_TRANSFER_ERROR = "Сумма перевода не должна превышать остаток в кассе или быть нулевой.\n" + TEMPLATE_SUM_TO_TRANSFER
TEMPLATE_TRANSFER_GENERAL_ERROR = "Ошибка при попытке перевода"
TEMPLATE_UPLOAD_SELECT_SERVICE = "Выберите вид коммунальных услуг для загрузки данных"
TEMPLATE_UPLOAD_SEND_FILE = "Отправьте файл с начислениями по услуге "
TEMPLATE_UPLOAD_SUCCESS = "Данные по начислениям были записаны в базу"
TEMPLATE_UPLOAD_ERROR = "Ошибка импорта данных"
TEMPLATE_STATE = ("За <b>{}</b> начислено:\n— аренда <b>{:.0f}€</b>\n— коммунальные услуги (за предыдущий месяц) <b>{:.0f}€</b>\n"
"— итого <b>{:.0f}€</b>\n\n Поступлений <b>{:.0f}€.</b>\n Остаток <b>{:.0f}€.</b>\n Занято квартир: <b>{}</b>.\n")
TEMPLATE_DEBTORS_ADM = ("За <b>{}</b> не было оплат:\n\n")
TEMPLATE_DEBTORS_ROW = "— {}, {}, @{}, {:.0f}€\n"
TEMPLATE_DEBTORS_NO_BALANCE_ROW = "— {}, {}, @{}\n"
TEMPLATE_FREE_APART_ADM = ("<b>{}</b>:\n")
TEMPLATE_FREE_APART_ROW = "— {} этаж: {}\n"
TEMPLATE_TENANT_OUT = "Оформить выезд жильца <b>{}</b> из квартиры <b>{}</b>?"
TEMPLATE_NO_TENANT = "В квартире {} никто не проживает. Проверьте указанный номер или обратитесь к администратору базы данных.\n"
TEMPLATE_TENANT_DONE = ("<b>{}</b> здесь больше не живет.\nВыселен из квартиры <b>{}</b>.\nRIP <b>{}</b> — <b>{}</b>.\n"
    "Был сделан пересчет аренды на сумму <b>{:.0f}€</b>, баланс с учетом пересчета <b>{:.0f}€</b>.")
TEMPLATE_COMMON_ERROR = "Сорян, братан, не сегодня. Зато погода хорошая. Может быть"
