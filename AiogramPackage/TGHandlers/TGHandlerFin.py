""" модерация группы в которой бот является админом"""

import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation
from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, del_kb
from aiogram.utils.markdown import hbold

fin_group_router = Router()
fin_group_router.message.filter(BOTFilterChatType(["private"]), BOTFilterFinList())


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


@fin_group_router.message(CommandStart())
@fin_group_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to fin start command details!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


@fin_group_router.message(Command("report", "rep", ignore_case=True))
@fin_group_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>reports!</b>")
    logging.info("requested reports")


@fin_group_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))
