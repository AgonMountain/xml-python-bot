""""""

"""База данных и компоненты для работы с ней"""
from engine.db_manager import DbManager
from data.config import DB_PATH
DB = DbManager(DB_PATH)

"""XML и компоненты для работы с ним"""
from engine.xml_manager import XmlTreeManager
from data.config import XML_PATH
XML = XmlTreeManager(XML_PATH)

"""Основные элементы vk_api для работы бота"""
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# TODO
configs = DB.get_all_configs()
messenger_id = DB.get_messenger_id('vk')

VK_BOT_TOKEN = None
for config in configs:
    if config[1] == messenger_id:
        VK_BOT_TOKEN = config[2]

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
        @param user_id идентификатор пользователя
        @param message сообщение для пользователей
        @param keyboard кнопки для пользователя
    """
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


"""Запускаем бота"""
for event in long_poll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            a = answer_generator.generate(DB, XML, messenger_id, event.user_id, event.text)
            send_message_to_user(event.user_id, a['message'], kb.get_keyboard_markup(a['button_text_list']))
