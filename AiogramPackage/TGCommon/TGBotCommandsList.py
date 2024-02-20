from aiogram.types import BotCommand

private_commands = [BotCommand(command="menu", description="Включить меню"),
                    BotCommand(command="hide_menu", description="Выключить меню"),
                    BotCommand(command="admin", description="Обновление списка пользователей"),
                    BotCommand(command="photo", description="Сохранить изображение"),
                    BotCommand(command="download", description="Получить изображение"),
                    BotCommand(command="report", description="Получить отчет")]
