from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

my_reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Меню"),
            KeyboardButton(text="О боте"),
            KeyboardButton(text="Реквизиты"),
            KeyboardButton(text="Платежные реквизиты"),
            KeyboardButton(text="Отчеты"),
        ],
    ]
)
