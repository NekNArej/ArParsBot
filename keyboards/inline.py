from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.utils import add_smth_to_base
import json

select_mode = InlineKeyboardMarkup(inline_keyboard=[
    [
    InlineKeyboardButton(
        text='Настройки ⚙️',
        callback_data='Settings'
        )],
    [InlineKeyboardButton(
        text='Клонировать 🐑',
        callback_data='clone'
    )]
])

reverse_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Со старых", callback_data='P_R_Old'),
    InlineKeyboardButton(text="С новых", callback_data='P_R_New')]
])



class FormParsing():
    def __init__(self, user_id: int, secret: bool |None = None, start_parsing: bool | None = None):
        with open('files/Data_base.json') as file:
            file = file.read()
            user = json.loads(file)[str(user_id)]
            self.donor_link = user['donor_link']
            self.target_link = user['target_link']
            self.reverse = user['reverse']
            self.limit = user['limit']
            self.secret = secret
            self.start_parsing = start_parsing

    def isLink(self, link: str):
        return '@' in link or 't.me' in link
        
    def donorLink(self) -> str:
        if self.donor_link:
            if self.isLink(self.donor_link):
                return f'{self.donor_link}        ✅'
            else:
                return f'{self.donor_link}        ❌'
        else:
            return f'Добавить ссылку на канал-донор'
        
    def targetLink(self) -> str:
        if self.target_link:
            if self.isLink(self.target_link):
                return f'{self.target_link}        ✅'
            else:
                return f'{self.target_link}        ❌'
        else:
            return f'Добавить ссылку на целевой канал'
        
    def SetReverse(self):
        if self.reverse:
            return 'Копировать первые: '
        else:
            return 'Копировать последние: '
    def StartParsing(self):
        if self.donor_link and self.target_link:
            return self.isLink(self.donor_link) and self.isLink(self.target_link)
        else:
            return False



    def finallyKeyBoard(self):
        buttons = [InlineKeyboardButton(text='Назад', callback_data='Back to Menu')]
        if self.StartParsing():
            buttons.append(
                InlineKeyboardButton(text='Поехали!', callback_data='P_Start')
            )
        
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text = self.donorLink(),
                callback_data= 'P_donor_link'
                )],
            [InlineKeyboardButton(
                text = self.targetLink(),
                callback_data = 'P_target_link'
            )],
            [
                InlineKeyboardButton(text=self.SetReverse(), callback_data='P_Reverse'),
                InlineKeyboardButton(text=self.limit, callback_data='P_Limit')
                ], 
            buttons
            ])    


class FormSettings():
    def __init__(self, user_id: str):
        with open('files/settings.json') as file:
            user = json.loads(file.read())[user_id]
            self.in_memory = user['in_memory']
    
    def inMemory(self):
        if self.in_memory:
            return 'Сохранять введённые значения'
        else:
            return 'Несохранять введённые значения'
    def showSettings(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text = self.inMemory(), callback_data='S_InMemory')],
            [InlineKeyboardButton(text='Назад', callback_data='Back to Menu')]
        ])