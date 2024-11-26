from telethon.sync import TelegramClient
from telethon.types import Message, MessageService

import os, sys
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)
from files.keys import API_ID, API_HASH
from utils.utils import getNumberFile


"""
from https://t.me/+e9W5dgobDgA1MjEy
to https://t.me/+83lizRo_ysE1OWQy
"""

def parsing(from_link: str, to_link: str, client: TelegramClient):
    right_id = ( client.get_entity(to_link)).id
    group_id = None
    media_group = []
    for message in client.iter_messages(from_link,reverse=True,limit=10,offset_id=7):
        if isinstance(message, MessageService):
            continue
        
        if message.grouped_id and not group_id:
            group_id = message.grouped_id
            file =  download(message, client)
            media_group = [message.message, file]
        elif group_id == message.grouped_id and group_id:
            file =  download(message, client)
            media_group.append(file)
        elif group_id:
            client.send_message(right_id, media_group[0], file=media_group[1:])
            for file in media_group:
                deleteFile(file)
            media_group = []
            group_id = message.grouped_id
            if group_id:
                # print('LOX')
                file =  download(message, client)
                media_group = [message.message, file]
            else:
                # file = download(message, client)
                file = 'download/video(1).mp4'
                client.send_message(right_id, message.message, file = file)
                deleteFile(file)
        else:
            # print('in')
            file =  download(message, client)
            f = client.send_message(right_id, message.message, file=file)
            print(f)
            deleteFile(file)
            



       
        
            
def deleteFile(path: str):
    if os.path.isfile(path):
        os.remove(path)

def download(message: Message, client: TelegramClient):
    # print(message)
    if not os.path.isdir('download'):
        os.makedirs('download')

    if 'photo' in dir(message.media):
        file =  client.download_media(message, file=f'download/photo({getNumberFile('photo','download/')}).png')
        return file
    elif 'video' in dir(message.media):
        file =  client.download_media(message, file=f'download/video({getNumberFile('video','download/')}).mp4')
        return file
    elif 'audio' in dir(message.media):
        file =  client.download_media(message, file=f'download/audio({getNumberFile('audio','download/')}).mp3')
        return file
    
    else:
        return None

def progress(curent, total):
    print('Uploaded',curent, 'out of', total, 'bytes: {:.2%}'.format(curent/total))
def main():
    # logging.basicConfig(level=logging.INFO)
    client = TelegramClient('ms', API_ID, API_HASH,
                        device_model='iPhone 55 Pro',
                        system_version='IOS 100.0')
    client.start()

    parsing(from_link='https://t.me/+e9W5dgobDgA1MjEy', to_link='https://t.me/+19fVSJhEBT9lNDJi', client=client)
    #  client.send_message('me', 'Hi',file='download/video(1).mp4')
    client.disconnect()
  

if __name__ == '__main__':
    main()

