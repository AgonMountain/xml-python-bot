"""Файл конфигурации"""

import os.path
from engine.xml_module.xml_manager import XmlManager
from engine.db_module.db_manager import DbManager


'''Токены для ботов'''
TM_BOT_TOKEN = '1606772582:AAHjEVXlN0kB6gOGwz2in08bsrhJeeNHljs'
VK_BOT_TOKEN = '06ba1aba1e021ddb67c512ccae7aa0bec52b5e1acbc1b127b0daf1eaf2cd50c167b2c8dcec8d87a29294f'

''''''
IDONTUNDERSTAND = "Извините, я Вас не понял. Пожалуйста, виберите один из вариантов ответа ниже."

'''XML документ'''
XML_PATH = '../../data/xml_data.xml'
XML = XmlManager(XML_PATH, 'branch', 'element')

'''База данных'''
DB_PATH = '../../data/db_data.db'
TM_TABLE_NAME = 'tm_user'
VK_TABLE_NAME = 'vk_user'

TM_DB = DbManager(os.path.abspath(os.path.join(DB_PATH)), TM_TABLE_NAME)
VK_DB = DbManager(os.path.abspath(os.path.join(DB_PATH)), VK_TABLE_NAME)
