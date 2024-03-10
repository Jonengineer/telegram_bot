from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
import configparser

config = configparser.ConfigParser()
config.read("C:\\bot\\analysis\\config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
session_file = 'C:\\bot\\analysis\\analizator2024.session'

with TelegramClient(session_file, api_id, api_hash) as client:
    client.start('0')
    channel_link = 'https://t.me/VPNsimpl'  # Замените ссылку на фактическую ссылку на канал
    entity = client.get_entity(channel_link)
    result = client(GetFullChannelRequest(entity.id))
    access_hash = result.chats[0].access_hash
    print(result)
    print(access_hash)