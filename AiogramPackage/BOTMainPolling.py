# from https://docs.aiogram.dev/en/latest/
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

from AiogramPackage.TGAlchemy.TGModelProd import create_table_async, drop_table_async, async_session
from AiogramPackage.TGConnectors.BOTMainClass import BOTMainClass
import logging

from AiogramPackage.TGHandlers.TGHandlerCallback import callback_router
from AiogramPackage.TGHandlers.TGHandlerUser import user_router
from AiogramPackage.TGHandlers.TGHandlerGroup import user_group_router
from AiogramPackage.TGHandlers.TGHandlerAdmin import admin_private_router
from AiogramPackage.TGHandlers.TGHandlerFin import fin_group_router
from AiogramPackage.TGCommon.TGBotCommandsList import private_commands
from AiogramPackage.TGMiddleWares.TGMWDatabase import DBMiddleware


logging.basicConfig(level=logging.INFO)
logging.info("logging starts")
bot_class = BOTMainClass()
_config = bot_class.get_main_config_json_data_sync()
logger = bot_class.logger
logger.brand = f"{os.path.basename(__file__)}"
logger.info(f"logger {os.path.basename(__file__)} starts logging")

ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

bot = Bot(token=_config.get("bot_config").get("token"), parse_mode=ParseMode.HTML)
dp = Dispatcher()

# version1 work after filter middleware
# admin_group_router.message.middleware(CounterMiddleware())
# version2 update in outer middleware all events before filters
# dp.update.outer_middleware(CounterMiddleware())

#0 router
# dp.include_router(callback_router)
#1 router
dp.include_router(admin_private_router)
#2 router
dp.include_router(fin_group_router)
#3 router
dp.include_router(user_router)
#4 router
dp.include_router(user_group_router)



bot.admins_list = [731370983]
bot.chat_group_admins_list = []
bot.fins_list = []
bot.restricted_words = []
async def on_startup(bot):
    run_param = False
    print("bot runs")
    if run_param:
        await drop_table_async()

    await create_table_async()

async def on_shutdown():
    print("Бот закрылся")
async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    # version3
    dp.update.middleware(DBMiddleware(session_pool=async_session))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    # version1 wuth list of updates
    # await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    # version2 with all uodates
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    logger.info(f"logger {os.path.basename(__file__)} starts logging")


if __name__ == '__main__':
    asyncio.run(main())
