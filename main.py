import os
import sys
import json
import time
import traceback

import telebot
import requests
import psutil


#     инициализация всякого

with open("config.json", "r") as json_settings:
    settings = json.load(json_settings)

TOKIN=settings["tokin"]


# Функция для мониторинга ресурсов
def monitor_resources():
    response_time,response_time,cpu_percent,ram_percent,disk_percent=0,0,0,0,0
    popitki=5
    popitka1=0
    #пинг в среднем 5 (можно изменять в popitki )попыток
    for i in range(popitki):
        start_time = time.time()
        response=requests.get('https://core.telegram.org/')
        if response.status_code==200:
            scode= ''
            pass
        else:
            scode=f" status code {response.status_code}"
        if i == 1:
            popitka1= time.time() - start_time
        response_time+= time.time() - start_time
        cpu_percent += float(psutil.cpu_percent())
        ram_percent +=float(psutil.virtual_memory().percent)
        if sys.platform.startswith('win'):
            disk_percent +=float(psutil.disk_usage('C:/').percent)
        else:
            disk_percent +=float(psutil.disk_usage('/').percent)
    shutka=' '
    if round(cpu_percent/popitki)==100:
        shutka='\nпроцессор шя рванет 🤯'
    return round(cpu_percent/popitki,1), round(ram_percent/popitki,1), round(disk_percent/popitki,1), str(str(round(response_time/popitki,3))+'s'+scode+shutka),round(popitka1,3)




bot = telebot.TeleBot(TOKIN ,num_threads=5)


@bot.message_handler(commands=['test'])
def monitor_test_command(message):
    test=''
    test+=os.getcwd()+'\n'
    swap = psutil.swap_memory()
    if os.path.exists(os.path.join(os.getcwd(), 'config.json')):
        test=test+'cofig file OK\n'
    else:
        test=test+'error no config file \n'
    test=test+f"ID> {message.from_user.id}\n"
    test=test+f"IP>{requests.get('https://api.ipify.org').content.decode('utf8')}\n"

    cpu_percent, ram_percent, disk_percent, response_time, ping1 = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}\n∟{ping1}\nфайл подкачки: {swap.percent}% ({swap.total / 1073741824:.2f} GB)\nadmin > {bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator','administrator']}\n\n{test}")
    
    


def main():
    get_num=0
    print("\033[32mнет ошибок :3\033[0m")
    while True:
        try:
            try:
                get_num=+1
                bot.polling(none_stop=True,timeout=30,long_polling_timeout=30,interval=1)
                if get_num >=100:
                    get_num=0
                    time.sleep(1)
            except requests.exceptions.ReadTimeout as e:
                print(f"time out ({e})")
            except requests.exceptions.ConnectionError as e:
                print(f"Error Connection ({e})\n{traceback.format_exc()}")
        except Exception as e:
            print(f"Ошибка: {e} \n-----------------------------\n{traceback.format_exc()}")
            time.sleep(3)
if __name__ == '__main__':
    main()