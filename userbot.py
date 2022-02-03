"""
Author:         DerPatayaner
Date:           03.02.2022
Last change:    03.02.2022

This script mirrors from one to another channel

usage: userbot.py [-h] api_id api_hash targetid mirrorid history

"""
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.patched import MessageService
import asyncio
import argparse 
import time
import random

parser = argparse.ArgumentParser()

parser.add_argument('api_id', type=int, help='Telegram API ID')
parser.add_argument('api_hash', help='Telegram API Hash')
parser.add_argument('targetid', type=int, help='Target group id to mirror from')
parser.add_argument('mirrorid', type=int, help='Mirror channel id')
parser.add_argument('history', help='Scrape full history (Yes/No)')

args = parser.parse_args()
api_id = args.api_id
api_hash = args.api_hash
mirror_from = args.targetid
mirror = args.mirrorid
history = args.history

client = TelegramClient("userbot.session", api_id, api_hash)
client.start()

loop = asyncio.get_event_loop()

async def get_full_history():
    """Mirror full chat history from one to another channel"""
    
    from_entity = await client.get_input_entity(mirror_from)
    to_entity = await client.get_input_entity(mirror)
    count = 0 

    async for message in client.iter_messages(from_entity, reverse=True):
        print(message)
        if isinstance(message, Message) and not isinstance(message, MessageService):
            if count == 250:
                time.sleep(300)
                count = 0
            await client.forward_messages(to_entity, message)
            wait = random.uniform(0.2,1.5)
            time.sleep(wait)
            count+=1

@client.on(events.NewMessage(mirror_from))
async def new_message_event(event):
    """Mirror all new Messages, except from MessageService events to another channel"""
    to_entity = await client.get_input_entity(mirror)
    if isinstance(event.message, Message) and not isinstance(event.message, MessageService):
        await event.forward_to(to_entity)

if __name__ == "__main__":
        if history.lower() == "yes":
            loop.run_until_complete(get_full_history())
        elif history.lower() != "no":
            logger.error("Please define history parameter")
            exit()
        client.run_until_disconnected()
