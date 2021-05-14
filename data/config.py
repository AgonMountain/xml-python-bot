"""Файл конфигурации"""
import os.path

'''Токены для ботов'''
TM_BOT_TOKEN = ''
VK_BOT_TOKEN = ''

''''''
IDONTUNDERSTAND = "Извините, я Вас не понял."

'''XML документ'''
XML_PATH = '../../data/xml_data.xml'
XML_PATH = os.path.abspath(os.path.join(XML_PATH))

XML_BRANCH_NAME_DEFAULT = 'Приверженность'
XML_ELEMENT_NAME_DEFAULT = '-1'


'''База данных'''
DB_PATH = '../../data/db_data.db'
DB_PATH = os.path.abspath(os.path.join(DB_PATH))

DB_TELEGRAM_TABLE_NAME = 'telegram_users'
DB_VK_TABLE_NAME = 'vk_users'
DB_ADMIN_TABLE_NAME = 'admins'
