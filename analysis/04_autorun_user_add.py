import time
import subprocess
import random

def run_script():
    # Здесь вызывается другой скрипт
    subprocess.run(['python', 'C:\\bot\\analysis\\03_user_add.py'])

while True:
    wait_time = random.randint(5500, 7500)
    wait_minutes = wait_time // 60
    print(f"Ожидание перед запуском скрипта: {wait_minutes} минут")
    
    time.sleep(wait_time)
    
    run_script()