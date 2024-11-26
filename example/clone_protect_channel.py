from pyrogram.enums import ParseMode, MessageMediaType

import logging
from pyrogram import Client
from typing import AsyncGenerator, List
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument
import asyncio


async def reversed_messages(messages: AsyncGenerator):
    reverse_messages = [message async for message in messages]
    return reverse_messages[::-1]
client = Client('Parser_Client')

async def clone_protect_content(donor_channel_id: int, my_channel_id: int):
    
    await client.start()
    logging.basicConfig(level=logging.INFO)

    messages: AsyncGenerator[Message, None] = client.get_chat_history(chat_id=donor_channel_id)

    reverse_messages: List[Message] = await reversed_messages(messages)

    for message in reverse_messages:
        # print(message)

        if message.text:
            await client.send_message(my_channel_id, message.text.html, parse_mode=ParseMode.HTML)
        elif message.media_group_id:
            messages: List[Message] = await client.get_media_group(chat_id=message.chat.id,
                                                                    message_id=message.id)
            # print(dir(message))
            if messages[0].id != message.id:
                continue
            media_group = await get_mg(messages=messages, client=client)
            await client.send_media_group(chat_id=my_channel_id, media=media_group)
        elif message.media:
            caption = message.caption.html if message.caption else None
            media = await message.download()
            if message.audio:
                await client.send_audio(my_channel_id, media, caption=caption, parse_mode=ParseMode.HTML)
            elif message.animation:
                await client.send_animation(my_channel_id, animation=media, caption=caption,
                                            parse_mode=ParseMode.HTML)
            elif message.document:
                await client.send_document(my_channel_id, document=media, caption=caption,
                                            parse_mode=ParseMode.HTML)
            elif message.photo:
                await client.send_photo(my_channel_id, media, caption, ParseMode.HTML)
            elif message.video:
                await client.send_video(my_channel_id, media, caption, ParseMode.HTML)
            elif message.video_note:
                await client.send_video_note(my_channel_id, media)
            elif message.voice:
                await client.send_voice(my_channel_id, media, caption, ParseMode.HTML)


async def get_mg(messages: List[Message], client: Client):
    media_group = []
    for message in messages:
        file = await message.download(in_memory=True)
        input_media = None
        caption = message.caption.html if message.caption else None
        if message.media == MessageMediaType.PHOTO:
            input_media = InputMediaPhoto(media=file, caption=caption, has_spoiler=message.has_media_spoiler,
                                          parse_mode=ParseMode.HTML)
        elif message.media == MessageMediaType.VIDEO:
            input_media = InputMediaVideo(media=file, caption=caption, has_spoiler=message.has_media_spoiler,
                                          parse_mode=ParseMode.HTML)
        elif message.media == MessageMediaType.AUDIO:
            input_media = InputMediaAudio(media=file, caption=caption, has_spoiler=message.has_media_spoiler,
                                          parse_mode=ParseMode.HTML)
        elif message.media == MessageMediaType.DOCUMENT:
            input_media = InputMediaDocument(media=file, caption=caption, has_spoiler=message.has_media_spoiler,
                                             parse_mode=ParseMode.HTML)
        media_group.append(input_media)

    return media_group


# if __name__ == '__main__':
#     for dialog in [ -4529204784,-1002168930868,-1002426864677,-1002398604736]:
#         asyncio.run(clone_protect_content(dialog,-1002290219828))

if __name__ == '__main__':
    asyncio.run(clone_protect_content(-1001917711554, -1002290219828))
