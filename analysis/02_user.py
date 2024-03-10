import asyncio
import configparser
from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from tqdm import tqdm
from telethon.tl.types import ChannelParticipantsSearch, InputUser
import os
from tqdm import tqdm

config = configparser.ConfigParser()
config.read("C:\\bot\\analysis\\config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']
session_file = 'C:\\bot\\analysis\\analizator2023.session'

async def dump_all_participants(channel, ChannelParticipantsSearch, client, GetParticipantsRequest):
    print('Сбор по каналу', channel.title)
    OFFSET_USER = 0
    LIMIT_USER = 500
    ALL_PARTICIPANTS = []
    FILTER_USER = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel, FILTER_USER, OFFSET_USER, LIMIT_USER, hash=0))
        if not participants.users:
            break
        ALL_PARTICIPANTS.extend(participants.users)
        OFFSET_USER += len(participants.users)

    with open(f"C:\\bot\\analysis\\log.txt", "w", encoding="utf-8") as write_file:
        for participant in tqdm(ALL_PARTICIPANTS):
            try:
                user = await client.get_entity(InputUser(participant.id, participant.access_hash))
                write_file.writelines(f" ID: {user.id} "
                                      f" First_Name: {user.first_name}"
                                      f" Last_Name: {user.last_name}"
                                      f" Username: {user.username}"
                                      f" Phone: {user.phone}"
                                      f" Access_Hash: {participant.access_hash}"  # Добавлен access_hash
                                      f" Channel: {channel.title} \n")
            except Exception as e:
                print(e)

    print('Сбор по каналу завершен')


async def main():
    async with TelegramClient(username, api_id, api_hash) as client:
        await client.start('0')
        with open("C:\\bot\\analysis\\links.txt", "r") as f:
            while True:
                try:
                    text = f.readline()
                    url = text.strip()
                    if not url:
                        break
                    channel = await client.get_entity(url)
                    print(url)
                    await dump_all_participants(channel, ChannelParticipantsSearch, client, GetParticipantsRequest)
                except Exception as e:
                    print(e)
        await client.disconnect()

async def run():
    await main()

input_file = "C:\\bot\\analysis\\log.txt"
target_substring = ["bot", "admin", "администратор", "..", "))", ")", "**", " . ", "//", "\\"]  # Список целевых подстрок

def remove_lines_with_substring(input_file, target_substring):
    count_deleted = 0
    # Открываем файл для чтения и создаем временный файл для записи
    with open(input_file, 'r', encoding='utf-8') as file, open('temp_file.txt', 'w', encoding='utf-8') as temp_file, tqdm(unit='line') as pbar:
        # Читаем файл построчно
        for line in file:
            # Проверяем, содержит ли строка целевую подстроку
            if not any(substring.lower() in line.lower() for substring in target_substring) and 'Phone: None' not in line:
                # Если не содержит, записываем строку во временный файл
                temp_file.write(line)
            else:
                count_deleted += 1  # Увеличиваем счетчик удаленных строк
    
            # Обновляем индикатор прогресса
            pbar.update(1)

    # Заменяем исходный файл временным файлом
    os.replace('temp_file.txt', input_file)

    # Проверяем наличие исходного файла после удаления
    if os.path.isfile(input_file):
        print("Удаление строк с подстрокой '{}' успешно завершено.".format(target_substring))
        print("Количество удаленных строк: {}".format(count_deleted))
    else:
        print("Ошибка при удалении строк с подстрокой '{}'.".format(target_substring))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    remove_lines_with_substring(input_file, target_substring)