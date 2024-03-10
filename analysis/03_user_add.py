from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest
import time
import random
import configparser

config = configparser.ConfigParser()
config.read("C:\\bot\\analysis\\config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
session_file = 'C:\\bot\\analysis\\analizator2023.session'

client = TelegramClient(session_file, api_id, api_hash)
client.start()

input_file = "C:\\bot\\analysis\\log.txt"
def extract_value(row, key):
    value = row.split(key, 1)[-1].strip().split(' ')[0]
    return value

users = []

with open(input_file, encoding='UTF-8') as f:
    rows = f.readlines()
    for row in rows:
        if ' ID: ' in row and ' Access_Hash: ' in row:
            user = {}
            user['id'] = int(extract_value(row, ' ID: '))
            user['access_hash'] = int(extract_value(row, ' Access_Hash: '))
            user['access_hash'] = int(extract_value(row, ' Access_Hash: '))
            users.append(user)
        else:
            print("Invalid data format in row:", row)

channel_id = 1665558558  # Замените YOUR_CHANNEL_ID на ID вашего канала VPN:1665558558
access_hash = -422743088833351719 # Замените YOUR_CHANNEL_ID на access_hash вашего канала VPN:  -422743088833351719
target_group_entity = InputPeerChannel(channel_id, access_hash)

def remove_lines_from_log():
    log_file = 'C:\\bot\\analysis\\log.txt'
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(log_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[17:])
    print("Удалили первые 17 записей")

n = 0

for user in users:
    n += 1
    try:
        user_to_add = InputPeerUser(user['id'], user['access_hash'])
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print(user)
        print("Ожидаем for 120-200 с")
        time.sleep(random.randrange(120, 200))

        if n >= 17:
            print("Добавили 17 пользователей. Скрипт останавливается.")
            remove_lines_from_log()
            break
    except Exception as e:
        print("Ошибка возникла:", e)

