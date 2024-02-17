# from https://docs.aiogram.dev/en/latest/
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
import logging

from AiogramPackage.TGHandlers.TGHandlerUser import user_router
from AiogramPackage.TGHandlers.TGHandlerGroup import user_group_router
from AiogramPackage.TGHandlers.TGHandlerAdmin import admin_group_router
from AiogramPackage.TGHandlers.TGHandlerFin import fin_group_router
from AiogramPackage.TGCommon.TGBotCommandsList import private_commands

logging.basicConfig(level=logging.INFO)
logging.info("logging starts")
bot_class = BOTMainClass()
_config = bot_class.get_main_config_json_data_sync()
logger = bot_class.logger
logger.brand = f"{os.path.basename(__file__)}"
logger.info(f"logger {os.path.basename(__file__)} starts logging")

ALLOWED_UPDATES = ["message", "edited_message"]

bot = Bot(token=_config.get("bot_config").get("token"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

#0 router
dp.include_router(admin_group_router)
#1 router
dp.include_router(fin_group_router)
#2 router
dp.include_router(user_router)
#3 router
dp.include_router(user_group_router)

bot.admins_list = [731370983]
bot.chat_group_admins_list = []
bot.fins_list = []
bot.restricted_words = []

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    logger.info(f"logger {os.path.basename(__file__)} starts logging")


if __name__ == '__main__':
    asyncio.run(main())
