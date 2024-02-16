import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.markdown import hbold
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilterChats import BOTFilterChat
from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards import TGKeybReplyBuilder as my_bld_kb


user_router = Router()
user_router.message.filter(BOTFilterChat(["private"]))

@user_router.message(CommandStart())
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kb.my_reply_kb)
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to bot!",
                         reply_markup=my_bld_kb.my_reply_kb_bld.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует"
                         ))


@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)


@user_router.message(Command("about", "abou", ignore_case=True))
@user_router.message((F.text.lower().contains("о боте")) | (F.text.lower().contains("бот")))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>company about!</b>",
                         reply_markup=my_bld_kb.my_reply_kb_bld_2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


@user_router.message(Command("details", "company", ignore_case=True))
@user_router.message(F.text.lower().contains("компан"))
async def menu_cmd(message: types.Message):
    text = as_list(as_marked_section(Bold("Реквизиты"), "1", "2", marker="·"), sep="\n-----")
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to company details!\n {text.as_html()}")
    logging.info("details reports")

@user_router.message(Command("account", "payments", ignore_case=True))
@user_router.message(F.text.lower().contains("платеж"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to account details!")
    logging.info(f"{hbold()}account details reports")
@user_router.message(Command("report", "rep", ignore_case=True))
@user_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>reports!</b>")
    logging.info("requested reports")
