""" модерация группы в которой бот является админом"""

import logging
import os

import aiofiles
from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f, IS_ADMIN
# from aiogram.filters.chat_member_updated import IS_ADMIN, ChatMemberUpdatedFilter, IS_MEMBER
from string import punctuation

from aiogram.types import BufferedInputFile

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType, BOTFilterFinList, BOTFilterIsGroupAdmin
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1_admin, del_kb
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns
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
async def menu_cmd(message: types.Message, bot: Bot):
    static_file = os.path.join(os.getcwd(), "data_static", "plot_img.jpg")
    async with aiofiles.open(static_file, "rb") as plot_img:
        await bot.send_photo(chat_id=message.chat.id,
                             photo=BufferedInputFile(file=await plot_img.read(), filename="График"),
                             caption=f"Здравствуйте, {hbold(message.from_user.first_name)}, добро пожаловать в <b>отчеты</b>!",
                             reply_markup=get_callback_btns(btns={
                                 "Прибыли/Убытки": "profit_report",
                                 "Баланс": "balance_report"}))

    logging.info("requested reports")


@fin_group_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{message.from_user.first_name}, welcome to admin main menu!",
                         reply_markup=reply_kb_lvl1_admin.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"))
