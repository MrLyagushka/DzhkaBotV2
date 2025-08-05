import asyncio
import logging

# Импорт библиотек
from aiogram import Dispatcher, Bot
# Импорт констант
from config import BOT_TOKEN
from handlers.profile import router_profile
from handlers.global_menu import router_command_start
from handlers.add_student import router_add_student
from handlers.task_bank import router_task_bank

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(router_command_start, router_profile, router_task_bank, router_add_student)
    await dp.start_polling(bot)


if __name__ == '__main__':
    file_log = logging.FileHandler('logging.log')
    console_out = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, handlers=(file_log, console_out))
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
        logging.info('Программа завершила работу по Ctrl + C')
    except Exception as exc:
        logging.info(f'{exc}')
