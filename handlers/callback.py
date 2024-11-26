from aiogram import Bot
from aiogram.types import CallbackQuery
from utils.utils import add_smth_to_base, active_function, lastBotMessage, Queue, Settings
from parser.main import start_parser
from keyboards.inline import FormParsing, FormSettings, reverse_inline, select_mode
import json

async def SwissCallBack(callback: CallbackQuery, bot: Bot):
    if callback.data[:2] == 'P_':
        await FormParsingCallback(callback, bot).CallbackManager()
    elif callback.data[:2] == 'S_':
        await FormSettingsCallback(callback, bot).CallbackManager()
    else:
        user_id = str(callback.from_user.id)
        match callback.data:
            case 'Back to Menu':
                text = 'Привет! Меня зовут ArPars, я могу скопировать любой канал так, чтобы никто об этом не узнал🤫'
                await bot.edit_message_text(text, chat_id=user_id, message_id=callback.message.message_id, reply_markup=select_mode)

            case 'clone':
                if add_smth_to_base(user_id) == 'Successfully' and Settings(user_id) == 'Successfully':
                    mes = await bot.edit_message_text( 'Ну что ж, начнём', chat_id=user_id, message_id=callback.message.message_id, reply_markup=FormParsing(user_id).finallyKeyBoard())
                    lastBotMessage(user_id, mes.message_id)
            case 'Settings':
                if Settings(user_id) == 'Successfully':
                    await bot.edit_message_text('Настройки', chat_id=user_id, message_id=callback.message.message_id, reply_markup=FormSettings(user_id).showSettings())

    


class FormParsingCallback():
    def __init__(self, callback: CallbackQuery, bot: Bot):
        self.callback = callback
        self.bot = bot
        self.user_id = str(callback.from_user.id)
        self.callback_data = callback.data
        self.message_id = callback.message.message_id

    async def CallbackManager(self):
        active_function(self.user_id, self.callback_data)
        match self.callback_data:
            case 'P_donor_link':
                text = 'Отправь мне ссылку на канал-донор'
            case 'P_target_link':
                text = 'Отправь мне ссылку на целевой канал'
            case 'P_Reverse':
                text = ''
                add_smth_to_base(self.user_id, reverse_reverse=True)
                # await self.bot.send_message(self.user_id, 'Откуда мне начать?', reply_markup=reverse_inline)
                await self.bot.edit_message_reply_markup(chat_id=self.user_id, message_id=self.message_id, reply_markup=FormParsing(self.user_id).finallyKeyBoard())
            # case 'P_R_Old':
            #     add_smth_to_base(self.user_id, reverse=True)
            #     text = 'edit'
            # case 'P_R_New':
            #     add_smth_to_base(self.user_id, reverse=False)
            #     text = 'edit'
            case 'P_Limit':
                text =  'Сколько будем копировать?'
            case 'P_Start':
                text = ''
                match Queue(self.user_id):
                    case self.user_id: 
                        await self.bot.send_message(self.user_id, 'Копирование началось')
                        await self.bot.send_message(self.user_id, await start_parser(user_id=self.user_id, bot = self.bot))
                    case 'Sleep':
                        return
                    case _:
                        await self.bot.send_message(self.user_id, 'Ваш запрос обрабатывается, ожидайте')
                                     
            case _:
                text = ''
                print(self.callback_data)


        match text:
            case 'edit':
                await self.bot.delete_message(self.user_id, self.callback.message.message_id)
                with open('files/last_message_id.json') as file:
                    file = file.read()
                    mes = json.loads(file)[self.user_id]
                    reply = FormParsing(self.user_id).finallyKeyBoard()
                    await self.bot.edit_message_text('Введите параметры', chat_id=self.user_id, message_id=mes, reply_markup=reply)
            case '':
                return
            case _ :
                await self.bot.send_message(self.user_id, text)

class FormSettingsCallback():
    def __init__(self, callback: CallbackQuery, bot: Bot):
        self.callback = callback
        self.bot = bot
        self.user_id = str(callback.from_user.id)
        self.callback_data = callback.data
        self.message_id = callback.message.message_id
    async def CallbackManager(self):

        match self.callback_data:
            case 'S_InMemory':
                if Settings(user_id=self.user_id, reverse_in_memory=True) == 'Successfully':
                    await self.bot.edit_message_reply_markup(chat_id=self.user_id, message_id=self.message_id, reply_markup=FormSettings(self.user_id).showSettings())