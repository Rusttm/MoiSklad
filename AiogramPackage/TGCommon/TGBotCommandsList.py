from aiogram.types import BotCommand

private_commands = [BotCommand(command="menu", description="Включить меню"),
                    BotCommand(command="hide_menu", description="Выключить меню"),
                    BotCommand(command="about", description="Информация о боте"),
                    BotCommand(command="company", description="Реквизиты Компании"),
                    BotCommand(command="account", description="Платежные реквизиты Компании"),
                    BotCommand(command="report", description="Получить отчет")]
