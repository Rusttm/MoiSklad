from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

my_reply_kb_bld = ReplyKeyboardBuilder()
my_reply_kb_bld.add(
    KeyboardButton(text="Меню"),
    KeyboardButton(text="Отчеты"),
    KeyboardButton(text="О боте"),
    KeyboardButton(text="Реквизиты Компании")
)
my_reply_kb_bld.adjust(2, 2)

my_reply_kb_bld_2 = ReplyKeyboardBuilder()
my_reply_kb_bld_2.attach(my_reply_kb_bld)
my_reply_kb_bld_2.row(
    KeyboardButton(text="Платежные реквизиты")
)