import os
import sys
import json
import time
import traceback

import telebot
import requests
import psutil
import subprocess

from libs.tpg_loger import logse


#     инициализация всякого

try:
    with open("config.json", "r") as json_settings:
        settings = json.load(json_settings)
except:
    with open("config.json", "w") as json_settings:
        json.dump(json_settings,{"tokin":" ","users":[5194033781]})
TOKIN=settings["tokin"]
USERS=list(settings["users"])

log=logse()
bot = telebot.TeleBot(TOKIN ,num_threads=5)


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


@bot.message_handler(commands=['test'])
def monitor_test_command(message):
    test=''
    test+=os.getcwd()+'\n'
    swap = psutil.swap_memory()
    if os.path.exists(os.path.join(os.getcwd(), 'config.json')):
        test=test+'cofig file OK\n'
    else:
        test=test+'error no config file \n'
    test=test+f"IP>{requests.get('https://api.ipify.org').content.decode('utf8')}\n"

    cpu_percent, ram_percent, disk_percent, response_time, ping1 = monitor_resources()
    bot.send_message(message.chat.id, f"CPU: {cpu_percent}%\nRAM: {ram_percent}%\nDisk: {disk_percent}%\nPing: {response_time}\n∟{ping1}\nфайл подкачки: {swap.percent}% ({swap.total / 1073741824:.2f} GB)\n\n{test}")
    
@bot.message_handler(commands=['ls','dir'])
def ls(message):
    buff=''
    for file in os.listdir():
        size=f"{os.path.getsize(file)} Байт"
        if type(size) != str and size>=1024:
            size=f"{round(size/1024, 1)} КБ"
        buff=buff+f"{file} {size}\n"
    bot.reply_to(message, buff)
    
@bot.message_handler(commands=['cd'])
def cd(message):
    dir=message.text.split(' ',1)[1]
    old_dir=os.getcwd()
    os.chdir(dir)
    bot.reply_to(message,f"{old_dir} -> {os.getcwd()}")
    
@bot.message_handler(commands=['pwd'])
def pwd(message):
    bot.reply_to(message,f"{os.getcwd()}")
    
@bot.message_handler(commands=['cmd','console'])
def console(message):
    if message.from_user.id not in USERS:
        bot.reply_to(message, "нет у вас досупа!")
        return
    try:        
        command=str(message.text).split(' ',1)[1]
        
        if sys.platform.startswith('win'):
            result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, text=True)
            out=result.stdout
        else:
            result=subprocess.run(command , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out=result.stdout + result.stderr 
                
            bot.reply_to(message, str(out))
    except:
        bot.reply_to(message,traceback.format_exc())

@bot.message_handler(commands=['download'])
def download_file(message):
    file=os.path.join(message.text.split(' ',1)[1])
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            bot.send_document(message.chat.id, f, reply_to_message_id=message.id)
            
@bot.message_handler(commands=['upload'])
def upload_file(message):
    if message.reply_to_message:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(os.path.join(os.getcwd(),message.document.file_name), 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "suppress ")
                
        elif message.photo:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(os.path.join(os.getcwd(), file_info.file_path), 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "suppress ")
                
        elif message.video:
            file_info = bot.get_file(message.video[len(message.video) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(os.path.join(os.getcwd(), file_info.file_path), 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "suppress ")
            
        else:
            bot.reply_to(message, "не подходящий тип сообщения")
    else:
        bot.reply_to(message, "команда должна быть ответом на дакумент для его загрузки")
    
    
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document','text', 'location', 'contact', 'sticker'])
def message_handler(message):
    #log message
    log.info(f"chat>> {message.chat.id} user>> {message.from_user.username} id>> {message.from_user.id}| сообщение >>\n{str(message.text if message.content_type == 'text' else message.content_type)}")


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
                log.error(f"time out ({e})")
            except requests.exceptions.ConnectionError as e:
                log.error(f"Error Connection ({e})\n{traceback.format_exc()}")
        except Exception as e:
            log.error(f"Ошибка: {e} \n-----------------------------\n{traceback.format_exc()}")
            time.sleep(3)
if __name__ == '__main__':
    main()