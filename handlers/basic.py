from aiogram import Bot
from aiogram.types import Message
from telethon import TelegramClient
from utils.utils import add_smth_to_base
from keyboards.inline import select_mode, FormParsing
from utils.commands import set_commands
from files.keys import ADMIN_ID, API_ID, API_HASH
import json
client = TelegramClient('ms', API_ID, API_HASH,
                        device_model='iPhone 55 Pro',
                        system_version='IOS 100.0')

async def bot_start(bot: Bot):
    await set_commands(bot)
    await bot.send_message(ADMIN_ID, 'bot start')




async def command_start(message: Message, bot: Bot):
    hello_message = 'Привет! Меня зовут ArPars, я могу скопировать любой канал так, чтобы никто об этом не узнал🤫'
    await bot.send_message(message.from_user.id, hello_message, reply_markup=select_mode)


async def register_text(message: Message, bot: Bot):
    user_id = str(message.from_user.id)
    text = message.text
    with open('files/Active_function_base.json') as file:
        file = file.read()
        users = json.loads(file)
        if user_id in users.keys():

            match users[user_id]:
                case 'P_donor_link':
                    add_smth_to_base(user_id,  donor_link=text)
                case 'P_target_link':
                    add_smth_to_base(user_id, target_link=text)
                case 'P_Reverse':
                    add_smth_to_base(user_id, reverse=text)
                case 'P_Limit':
                    add_smth_to_base(user_id, limit=text)
                case _:
                    print(users[user_id])
            await bot.delete_messages(user_id, [message.message_id, message.message_id-1])
            with open('files/last_message_id.json') as file:
                file = file.read()
                mes = json.loads(file)[user_id]
                reply = FormParsing(user_id).finallyKeyBoard()
                await bot.edit_message_text('Введите параметры', chat_id=user_id, message_id=mes, reply_markup=reply)
