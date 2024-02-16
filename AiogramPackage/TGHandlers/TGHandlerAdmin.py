""" модерация группы в которой бот является админом"""

import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation
from AiogramPackage.TGFilters.BOTFilterChats import BOTFilterChat, BOTFilterFin
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_bld_admin
from aiogram.utils.markdown import hbold

admin_group_router = Router()
admin_group_router.message.filter(BOTFilterFin())

restricted_words = {"идиот", "дурак", "хрень", "idiot"}


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


@admin_group_router.message(CommandStart())
@admin_group_router.message(F.text.lower() == "start")
async def admin_menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to admin start command details!",
                         reply_markup=reply_kb_bld_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


@admin_group_router.message(Command("report", "rep", ignore_case=True))
@admin_group_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>reports!</b>")
    logging.info("requested reports")
