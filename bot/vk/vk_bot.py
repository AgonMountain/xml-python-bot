import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from data.config import VK_DB, XML, VK_BOT_TOKEN, IDONTUNDERSTAND
from bot.vk.vk_keyboard import VkKeyboard

vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
session_api = vk_session.get_api()
long_poll = VkLongPoll(vk_session)
kb = VkKeyboard()


def send_message_to_user(user_id, message, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})


for event in long_poll.listen():

    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            user_id = event.user_id

            if VK_DB.get_current_element_id(user_id) == None:
                VK_DB.add(user_id)

            element = XML.get_element_by_id(VK_DB.get_current_element_id(user_id))

            message = element.text.text

            transition_list = element.transition_list
            addition_list = element.addition_list

            understand_flag = False

            for transition in transition_list:
                if event.text == transition.text:
                    understand_flag = True
                    next_element_id = transition.get('next_element_name')
                    VK_DB.update_current_element_id(user_id, next_element_id)

                    element = XML.get_element_by_id(next_element_id)
                    message = XML.get_element_by_id(next_element_id).text.text
                    transition_list = element.transition_list
                    addition_list = element.addition_list
                    break

            if not understand_flag:
                for addition in addition_list:
                    if event.text == addition.text:
                        understand_flag = True
                        element_id = addition.get('element_name')
                        message = XML.get_element_by_id(element_id).text.text
                        break

            if not understand_flag and element.id != '-1':
                message = IDONTUNDERSTAND

            transition_text_list = [transition.text for transition in transition_list]
            addition_text_list = [addition.text for addition in addition_list]
            button_text_list = transition_text_list + addition_text_list

            keyboard = kb.get_keyboard_markup(button_text_list)

            send_message_to_user(user_id, message, keyboard)
