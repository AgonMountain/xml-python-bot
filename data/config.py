"""Файл конфигурации"""
import os.path

'''Токены для ботов'''
TM_BOT_TOKEN = '1606772582:AAHjEVXlN0kB6gOGwz2in08bsrhJeeNHljs'
VK_BOT_TOKEN = '06ba1aba1e021ddb67c512ccae7aa0bec52b5e1acbc1b127b0daf1eaf2cd50c167b2c8dcec8d87a29294f'

''''''
IDONTUNDERSTAND = "Извините, я Вас не понял. Пожалуйста, виберите один из вариантов ответа ниже."

'''XML документ'''
XML_PATH = '../data/xml_data.xml'
XML_PATH = os.path.abspath(os.path.join(XML_PATH))

XML_BRANCH_NAME_DEFAULT = 'Приверженность'
XML_ELEMENT_NAME_DEFAULT = '-1'


'''База данных'''
DB_PATH = '../data/db_data.db'
DB_PATH = os.path.abspath(os.path.join(DB_PATH))

DB_TELEGRAM_TABLE_NAME = 'telegram_users'
DB_VK_TABLE_NAME = 'vk_users'
DB_ADMIN_TABLE_NAME = 'admins'
