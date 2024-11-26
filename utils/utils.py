import os, sys
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)
from telethon import TelegramClient as asyncTelegramClient
from telethon.sync import TelegramClient
from telethon.types import Message as MessageClient
from files.keys import *
import asyncio
from aiogram.types import Message as MessageBot
from aiogram import Bot
import json
async def asyncGetCorrectId(id: int, client = asyncTelegramClient) -> int | str:
    try:
        await client.get_entity(id)
        return(id)
    except:
        try:
            new_id = int(f'-{id}')
            await client.get_entity(new_id)
            return(new_id)
        except:
            try:
                new_id = int(f'-100{id}')
                await client.get_entity(new_id)
                return(new_id)
            
            except Exception as e:
                print(e)
                return 'Error'
            
def getCorrectId(id: int, client = TelegramClient) -> int | str:
    try:
        client.get_entity(id)
        return(id)
    except:
        try:
            new_id = int(f'-{id}')
            client.get_entity(new_id)
            return(new_id)
        except:
            try:
                new_id = int(f'-100{id}')
                client.get_entity(new_id)
                return(new_id)
            
            except Exception as e:
                print(e)
                return 'Error'


async def downloadMedia(message: MessageClient, client: asyncTelegramClient):
    if message.photo:

        file = await client.download_media(message.photo)
        return file
    pass
            
async def getNumberFile(type: str, path = './') -> int:
    my_dir = os.listdir(path)[::-1]
    for file in my_dir:
        if type in file:
            return int(file[len(type)+12:-5]) + 1
    else:
        return 1
    
def delete_task(user_id: int|str):
      
    with open('files/Data_base.json', 'r') as file:
        file = file.read()
        clients = json.loads(file)
        del clients[user_id]
    with open('files/Data_base.json', 'w') as file:
        clients = json.dumps(clients)
        file.write(clients)


def add_smth_to_base(
        user_id: str,
        donor_link: str = None,
        target_link: str = None,
        reverse_reverse: bool = False,
        limit: str = None):
    
    user_id = str(user_id)
    if not os.path.isdir('files'): #Создает файл базы данных
        os.makedirs('files')
    if not os.path.exists('files/Data_base.json'):
        open('files/Data_base.json','w').close()

    with open('files/Data_base.json') as file:
        clients = file.read()
        if clients != '':
            clients = json.loads(clients)
            if user_id in clients.keys(): #and [donor_link, target_link, reverse, limit].count(None) < 4:
                client = clients[user_id]
            else:
                client = {
                'donor_link': None,
                'target_link': None,
                'reverse': False,
                'limit': '10'}
        
        else:
            clients = {user_id: {
                'donor_link': None,
                'target_link': None,
                'reverse': False,
                'limit': '10'}}
            client = clients[user_id]
        client_copy = client
        if donor_link:
            client['donor_link'] = donor_link
        elif target_link:
            client['target_link'] = target_link
        elif reverse_reverse:
            client['reverse'] = not client['reverse']
        elif limit:
            client['limit'] = limit
        if client_copy == client and ( [donor_link, target_link, limit].count(None) < 4 or reverse_reverse):
            if client['limit'][0] == ' ':
                client['limit'] = f'{int(client['limit'])}'
            else:
                client['limit'] = f' {client['limit']} '
        clients[user_id] = client
    with open('files/Data_base.json','w+') as file:
        clients = json.dumps(clients)
        file.write(clients)
        return 'Successfully'

def active_function(user_id: int | str, function_name: str):
    user_id = str(user_id)
    if not os.path.isdir('files'): #Создает файл базы данных
        os.makedirs('files')
    if not os.path.exists('files/Active_function_base.json'):
        open('files/Active_function_base.json','w').close()

    with open('files/Active_function_base.json') as file: 
        file = file.read()
        if file != '':
            users = json.loads(file)
            users[user_id] = function_name
        else:
            users = {user_id: function_name}
        users = json.dumps(users)
    with open('files/Active_function_base.json', 'w') as file:
        file.write(users)


def lastBotMessage(user_id: int | str, message_id: int | str):
    user_id = str(user_id)
    message_id = int(message_id)
    if not os.path.isdir('files'): #Создает файл базы данных
        os.makedirs('files')
    if not os.path.exists('files/last_message_id.json'):
        open('files/last_message_id.json','w').close()

    with open('files/last_message_id.json') as file:
        file = file.read()
        if file != '':
            users = json.loads(file)
            users[user_id] = message_id
        else:
            users = {user_id: message_id}
        users = json.dumps(users)
    with open('files/last_message_id.json', 'w') as file:
        file.write(users)

def Queue(user_id: str = None, remove: bool = False):
    if not os.path.isdir('files'):
        os.mkdir('files')
    if not os.path.isfile('files/queue.json'):
        open('files/queue.json', 'w').close()
    with open('files/queue.json', 'r+') as file:
        queue = file.read()
        len_queue = 0
        if queue != '':
            queue= queue.split('  ')[0]
            len_queue = len(queue)
            queue = json.loads(queue)
            if user_id and not remove:
                queue.append(user_id)
            elif user_id in queue and remove:
                queue.remove(user_id)
        else:
            if user_id and not remove:
                queue = [user_id]
            else:
                queue = []
        queue_dumps = json.dumps(queue)
        if len(queue_dumps) < len_queue:
            queue_dumps += ' ' * (len_queue - len(queue))
        file.seek(0)
        file.write(queue_dumps)
        # print(type(queue_f), queue_f, queue)
        if queue != []:
            return queue[0]
        else:
            return 'Sleep'

def Settings(user_id: str, reverse_in_memory: bool = False):
    if not os.path.isdir('files'):
        os.mkdir('files')
    if not os.path.isfile('files/settings.json'):
        open('files/settings.json', 'w').close()
    with open('files/settings.json', 'r+') as file:
        users = file.read()
        len_users = 0
        if users != '':
            users = users.split('  ')[0]
            len_users = len(users)
            users = json.loads(users)
            if user_id in users.keys():
                user = users[user_id]
            else:
                user = {
                    'in_memory': False
                }
        else:
            users = {user_id: {
                'in_memory': False
                }}
            user = users[user_id]
        if reverse_in_memory:
            user['in_memory'] = not user['in_memory']
        users[user_id] = user
        users_dumps = json.dumps(users)
        if len(users_dumps) < len_users:
            users_dumps += ' '*(len_users - len(users_dumps))
        file.seek(0)
        file.write(users_dumps)
        return 'Successfully'
        
    






























async def main():
    client = TelegramClient('Astls', API_ID, API_HASH)
    await client.start()
    for id in [4053146990,1632839884,4520800312,1387766713,2476130529]:
        print(id, await getCorrectId(id, client))
    # print(await client.get_entity(-4053146990))
    await client.disconnect()

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())