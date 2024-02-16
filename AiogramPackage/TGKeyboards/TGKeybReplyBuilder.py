from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

my_reply_kb_bld = ReplyKeyboardBuilder()
my_reply_kb_bld.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="Платежные реквизиты"),
    KeyboardButton(text="О боте"),
    KeyboardButton(text="Реквизиты Компании")
)
my_reply_kb_bld.adjust(2, 2)

reply_kb_bld_admin = ReplyKeyboardBuilder()
reply_kb_bld_admin.attach(my_reply_kb_bld)
reply_kb_bld_admin.row(
    KeyboardButton(text="Отчеты")
)

del_kb = ReplyKeyboardRemove()


def get_my_kb(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2, 2),
):
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
