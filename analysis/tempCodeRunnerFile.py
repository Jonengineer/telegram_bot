import time
import subprocess
import random

def run_script():
    # Здесь вызывается другой скрипт
    subprocess.run(['python', 'C:\\bot\\analysis\\03_user_add.py'])

while True:
    run_script()
    # Генерация случайного времени ожидания в диапазоне от 60 до 90 минут (в секундах)
    wait_time = random.randint(3600, 5500)
    time.sleep(wait_time)