from files.keys import TOKEN
from aiogram import Bot, Dispatcher, F
import asyncio, logging
from aiogram.filters import CommandStart, Command
from handlers.basic import *
from handlers.callback import SwissCallBack


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.startup.register(bot_start)
    dp.message.register(command_start, CommandStart())
    # dp.message.register(start_parser, Command(commands=['/start_parsing']))
    dp.message.register(register_text)
    # dp.callback_query.register(clone_callback, F.data == 'clone')
    dp.callback_query.register(SwissCallBack)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        quit()
