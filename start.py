import subprocess, os.path, time
import webbrowser
from engine.db_manager import DbManager
from engine.convertor import Convertor

DB_PATH = os.path.abspath(os.path.join('../webserver/db.sqlite3'))
XML_PATH = os.path.abspath(os.path.join('../data/xml_data.xml'))
TM_BOT_PATH = os.path.abspath(os.path.join('../bot/tm/tm_bot.py'))
VK_BOT_PATH = os.path.abspath(os.path.join('../bot/vk/vk_bot.py'))
WEBSERVER_PATH = os.path.abspath(os.path.join('../webserver/manage.py'))

DB = DbManager(DB_PATH)

tmbot = None
telegram_config = DB.get_config('tm')
old_telegram_token = ''

vkbot = None
vk_config = DB.get_config('vk')
old_vk_token = ''


webserver = subprocess.Popen(['python', WEBSERVER_PATH, 'runserver'])
if webserver:
    print('Сервер запущен - ' + str(time.ctime()))
    webbrowser.open('http://127.0.0.1:8000/', new=2)
    print('Открыта страница для администратора - ' + str(time.ctime()))

while True:
    print('Проверка на необходимость обновления - ' + str(time.ctime()))
    need_update_for_xml = DB.get_need_for_update_xml()
    telegram_config = DB.get_config('tm')
    vk_config = DB.get_config('vk')

    if need_update_for_xml:

        DB.update_config(telegram_config['id'], telegram_config['token'], 0)
        DB.update_config(vk_config['id'], vk_config['token'], 0)
        print('Бот Телеграм и Бот Вконтакте отключены перед обновлением XML файла - ' + str(time.ctime()))

        Convertor.convert_from_db_to_xml(DB_PATH, XML_PATH)
        DB.update_need_for_update_xml(0)
        print('XML файл был обновлен - ' + str(time.ctime()))

        if vkbot != None:
            tmbot.terminate()
        tmbot = subprocess.Popen(['python', TM_BOT_PATH])

        if vkbot != None:
            vkbot.terminate()
        vkbot = subprocess.Popen(['python', VK_BOT_PATH])

        DB.update_config(telegram_config['id'], telegram_config['token'], 1)
        DB.update_config(vk_config['id'], vk_config['token'], 1)
        print('Бот Телеграм и Бот Вконтакте включены - ' + str(time.ctime()))

    if old_telegram_token != telegram_config['token']:
        if tmbot != None:
            tmbot.terminate()
        tmbot = subprocess.Popen(['python', TM_BOT_PATH])
        old_telegram_token = telegram_config['token']
        print('Токен для бота Телеграм был обновлен - ' + str(time.ctime()))

    if old_vk_token != vk_config['token']:
        if vkbot != None:
            vkbot.terminate()
        vkbot = subprocess.Popen(['python', VK_BOT_PATH])
        old_vk_token = vk_config['token']
        print('Токен для бота Вконтакте был обновлен - ' + str(time.ctime()))

    time.sleep(30)
