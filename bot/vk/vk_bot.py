""""""

"""База данных и компоненты для работы с ней"""
from engine.db_manager import DbManager
from data.config import DB_PATH, DB_VK_TABLE_NAME
VK_DB = DbManager(DB_PATH, DB_VK_TABLE_NAME)

"""XML и компоненты для работы с ним"""
from engine.xml_manager import XmlTree
from data.config import XML_PATH
XML = XmlTree(XML_PATH)

"""Основные элементы vk_api для работы бота"""
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from data.config import VK_BOT_TOKEN
vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)

"""Клавиатура и генератор ответов для бота"""
from bot.vk.vk_keyboard import VkKeyboard
from bot import answer_generator
kb = VkKeyboard()


def send_message_to_user(user_id, message, keyboard):
    """
        Отправить сообщение пользователю
        > user_id идентификатор пользователя
        > message сообщение для пользователей
        > keyboard кнопки для пользователя
    """
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


"""Запускаем бота"""
for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            a = answer_generator.generate(VK_DB, XML, event.user_id, event.text)
            send_message_to_user(event.user_id, a['message'], kb.get_keyboard_markup(a['button_text_list']))
