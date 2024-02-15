import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from AiogramPackage.TGFilters.BOTFilterChats import BOTFilterChat
from AiogramPackage.TGKeyboards import TGKeybReply as my_reply_kbds


user_router = Router()
user_router.message.filter(BOTFilterChat(["private"]))

@user_router.message(CommandStart())
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kbds.my_reply_kb)


@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kbds.del_kb)


@user_router.message(Command("about", "abou", ignore_case=True))
@user_router.message((F.text.lower().contains("инфо")) | (F.text.lower().contains("о нас")))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to about!")

@user_router.message(Command("details", "company", ignore_case=True))
@user_router.message(F.text.lower().contains("реквизиты"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to company details!")
    logging.info("details reports")

@user_router.message(Command("account", "payments", ignore_case=True))
@user_router.message(F.text.lower().contains("платеж"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to account details!")
    logging.info("account details reports")
@user_router.message(Command("report", "rep", ignore_case=True))
@user_router.message(F.text.lower().contains("отчет"))
async def menu_cmd(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, welcome to reports!")
    logging.info("requested reports")
