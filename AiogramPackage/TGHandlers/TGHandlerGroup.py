""" модерация группы в которой бот является админом"""

import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from string import punctuation
from AiogramPackage.TGFilters.BOTFilterChats import BOTFilterChat


user_group_router = Router()
user_group_router.message.filter(BOTFilterChat(["group", "supergroup"]))

restricted_words = {"идиот", "дурак", "хрень", "idiot"}


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    message_words_set = set(clean_text(message.text.lower()).split())
    if restricted_words.intersection(message_words_set):
        await message.answer(f"{message.from_user.username}, соблюдайте порядок в чате!")
        await message.delete()
        # можно даже забанить
        # await message.chat.ban(message.from_user.id)
        # и потом восстановить
        # await message.chat.unban(message.from_user.id)


