from telethon import TelegramClient
from telethon.types import ReplyInlineMarkup, KeyboardButtonSwitchInline, KeyboardButtonRow
import asyncio
from files.keys import *


async def main():
    bot = TelegramClient('bot', API_ID, API_HASH)
    await bot.start()
    murkup = ReplyInlineMarkup([
        [KeyboardButtonSwitchInline('Привет', query='sound')]
    ])
    reply_markup=ReplyInlineMarkup([KeyboardButtonRow(buttons=[KeyboardButtonSwitchInline(text='✉️ Рекомендовать другу', query='#share 12791993 ')])])
    await bot.send_message(ADMIN_ID, 'Hello', buttons=reply_markup)











if __name__ == "__main__":
    asyncio.run(main())


