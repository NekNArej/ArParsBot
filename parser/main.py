from telethon import TelegramClient
from telethon.types import Message, MessageService
from aiogram import Bot
import os, sys, json
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)
from files.keys import API_ID, API_HASH
from utils.utils import getNumberFile, delete_task, Queue


"""
from https://t.me/+e9W5dgobDgA1MjEy
to https://t.me/+83lizRo_ysE1OWQy
"""

async def start_parser(user_id: str, bot: Bot):
    client = TelegramClient('ms', API_ID, API_HASH,
                        device_model='iPhone 55 Pro',
                        system_version='IOS 100.0')
    user_id = str(user_id) 
    with open('files/Data_base.json') as file:
        file = file.read()
        users = json.loads(file)
        user = users[user_id]
        donor_link = user["donor_link"]
        target_link = user['target_link']
        reverse = user['reverse']
        limit = user['limit']
    
    async with client:
        result = await parsing(client = client, user_id = user_id, donor_link=donor_link, target_link=target_link, reverse=reverse, limit=limit)
    if result == 'Successfully':
        with open('files/settings.json') as file:
            user = json.loads(file.read())[user_id]
            if not user['in_memory']:
                delete_task(str(user_id))
        result_queue = Queue(user_id, remove=True)
        if  result_queue != 'Sleep':
            
            await bot.send_message(result_queue, 'Копирование началось')
            await bot.send_message(result_queue, await start_parser(result_queue, bot))



    return result


async def parsing(client: TelegramClient, user_id: str, donor_link: str, target_link: str, reverse=True, limit=10):
    limit =int(limit)
    right_id = (await client.get_entity(target_link)).id
    group_id = None
    media_group = []
    async for message in client.iter_messages(donor_link, reverse=reverse, limit=limit):
        message: Message
        if isinstance(message, MessageService): #Исключаем СЕРВИСНЫЕ сообщения
            continue
        if message.grouped_id and group_id is None:
            group_id = message.grouped_id
            file = await download(user_id, message, client)
            media_group = [message.message, file]
        elif group_id == message.grouped_id and group_id:
            file = await download(user_id, message, client)
            media_group.append(file)
        elif group_id:
            print('sending...') #Сделать прогресс бар
            await client.send_message(right_id, media_group[0], file=media_group[1:])
            for file in media_group:
                deleteFile(file)
            media_group = []
            group_id = message.grouped_id
            if group_id:
                file = await download(user_id, message, client)
                media_group = [message.message, file]
            else:
                file = await download(user_id, message, client)
                await client.send_message(right_id, message.message, file = file)
                deleteFile(file)
        else:
            file = await download(user_id, message, client)
            await client.send_message(right_id, message.message, file=file)
            deleteFile(file)
    else:
        if media_group != []:
            print('sending...')
            await client.send_message(right_id, media_group[0], file=media_group[1:])
            for file in media_group:
                deleteFile(file)
            media_group = []
            group_id = None
    return 'Successfully'
            




        
            
def deleteFile(path: str):
    path = str(path)
    if os.path.isfile(path):
        os.remove(path)

async def download(user_id: int, message: Message, client: TelegramClient, ):
    user_id = user_id
    if not os.path.isdir('download'):
        os.makedirs('download')
    if 'photo' in dir(message.media):
        file = await client.download_media(message, file=f'download/photo_{user_id}({await getNumberFile('photo','download/')}).png')
        return file
    elif 'video' in dir(message.media):
        file = await client.download_media(message, file=f'download/video_{user_id}({await getNumberFile('video','download/')}).mp4')
        return file
    elif 'audio' in dir(message.media):
        file = await client.download_media(message, file=f'download/audio_{user_id}({await getNumberFile('audio','download/')}).mp3')
        return file
    
    else:
        return None


