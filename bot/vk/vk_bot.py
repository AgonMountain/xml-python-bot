import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from data.config import VK_DB, XML, VK_BOT_TOKEN
from bot.vk.vk_keyboard import VkKeyboard
from bot import answer_generator

"""Основные элементы vk_api для работы бота"""
vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)
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
