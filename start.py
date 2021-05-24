import subprocess, os.path, time
import webbrowser
from engine.db_manager import DbManager
from engine.convertor import Convertor

DB_PATH = os.path.abspath(os.path.join('../webserver/db.sqlite3'))
XML_PATH = os.path.abspath(os.path.join('../data/xml_data.xml'))

DB = DbManager(DB_PATH)

tmbot = None
telegram_config = DB.get_config('tm')
old_telegram_token = ''

vkbot = None
vk_config = DB.get_config('vk')
old_vk_token = ''


webserver = subprocess.Popen(['python', '../webserver/manage.py', 'runserver'])
if webserver:
    print('Сервер запущен - ' + str(time.ctime()))
    webbrowser.open('http://127.0.0.1:8000/admin/', new=2)
    print('Открыта страница для администратора - ' + str(time.ctime()))

while True:
    telegram_config = DB.get_config('tm')
    need_update_for_xml = DB.get_need_for_update_xml()

    if need_update_for_xml:
        Convertor.convert_from_db_to_xml(DB_PATH, XML_PATH)
        DB.update_need_for_update_xml(0)

    if old_telegram_token != telegram_config['token']:
        if vkbot != None:
            tmbot.terminate()
        tmbot = subprocess.Popen(['python', '../bot/tm/tm_bot.py'])
        old_telegram_token = telegram_config['token']
        print('Токен для бота Телеграм был обновлен - ' + str(time.ctime()))

    vk_config = DB.get_config('vk')
    if old_vk_token != vk_config['token']:
        if vkbot != None:
            vkbot.terminate()
        vkbot = subprocess.Popen(['python', '../bot/vk/vk_bot.py'])
        old_vk_token = vk_config['token']
        print('Токен для бота Вконтакте был обновлен - ' + str(time.ctime()))

    print('Проверка на необходимость обновления - ' + str(time.ctime()))
    time.sleep(60)
