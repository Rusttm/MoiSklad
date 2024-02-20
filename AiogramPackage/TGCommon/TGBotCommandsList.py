from aiogram.types import BotCommand

private_commands = [BotCommand(command="menu", description="Включить меню"),
                    BotCommand(command="hide_menu", description="Выключить меню"),
                    BotCommand(command="admin", description="Загрузка списка пользователей"),
                    BotCommand(command="photo", description="Загрузка фотографии"),
                    BotCommand(command="account", description="Платежные реквизиты Компании"),
                    BotCommand(command="report", description="Получить отчет")]
