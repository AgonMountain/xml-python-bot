from data.config import IDONTUNDERSTAND, XML_BRANCH_NAME_DEFAULT, XML_ELEMENT_NAME_DEFAULT
from data.config import DB_PATH, XML_PATH
from engine.db_manager import DbManager
from engine.xml_manager import XmlTreeManager


def generate(is_on, DB, XML, messenger_id, user_id, message_text):
    """
    Сформировать ответ для пользователя
    > DB база данных пользователей, где хранятся данные рассматриваемого пользователя
    > XML данные схем для общения с пользователем
    > user_id идентификатор пользователя
    > message_text сообщение от пользователя в виде текста
    return out ответное сообщение out['message'] и список слов для кнопок out['button_text_list']
    """

    '''переменные функции'''
    out = {'message': None, 'button_text_list': None}
    out['message'] = IDONTUNDERSTAND
    stop_loop_flag = False  # незачем крутить циклы впустую

    if is_on:
        '''актуальные данные пользователя'''
        user_data = DB.get_user_data(user_id)

        '''нет пользователя в бд -> создаем его и задаем значение по умолчанию'''
        if user_data == None:
            element_id = DB.get_element_id(XML_ELEMENT_NAME_DEFAULT)
            DB.add_user(user_id, element_id, messenger_id)

            user_data = DB.get_user_data(user_id)
            current_element = DB.get_element_data(user_data['element_id'])
            current_branch_name = DB.get_scheme_data(current_element['scheme_id'])['name']
            current_element_name = current_element['name']

            XML.switch_scheme(current_branch_name)
            element = XML.convert_element(XML.get_element(current_element_name))
            out['message'] = element.text.text
            stop_loop_flag = True
        else:
            current_element = DB.get_element_data(user_data['element_id'])
            current_branch_name = DB.get_scheme_data(current_element['scheme_id'])['name']
            current_element_name = current_element['name']
            XML.switch_scheme(current_branch_name)
            element = XML.convert_element(XML.get_element(current_element_name))

        '''списки текстов переходов и текстов дополнений'''
        transition_list = element.transition_list
        addition_list = element.addition_list

        '''поиск совпадения: сообщение от пользователя == текст перехода'''
        if not stop_loop_flag:
            for transition in transition_list:
                if message_text == transition.text:
                    next_branch_name = transition.get('scheme_name')
                    next_element_name = transition.get('element_name')

                    DB.update_user(user_id, DB.get_element_id(next_element_name))

                    XML.switch_scheme(next_branch_name)
                    element = XML.convert_element(XML.get_element(next_element_name))
                    out['message'] = element.text.text

                    transition_list = element.transition_list
                    addition_list = element.addition_list

                    stop_loop_flag = True
                    break

        '''поиск совпадения: сообщение от пользователя == текст дополнения'''
        if not stop_loop_flag:
            for addition in addition_list:
                if message_text == addition.text:
                    branch_name = addition.get('scheme_name')
                    element_name = addition.get('element_name')

                    XML.switch_scheme(branch_name)
                    element = XML.convert_element(XML.get_element(element_name))
                    out['message'] = element.text.text

                    break

        transition_text_list = [transition.text for transition in transition_list]
        addition_text_list = [addition.text for addition in addition_list]
        out['button_text_list'] = transition_text_list + addition_text_list

        '''пользователь ответил что-то непонятное, говорим ему об этом + повторяем вопрос и варианты ответов'''
        if out['message'] == IDONTUNDERSTAND:
            out['message'] += '\n\nПожалуйста, ответить на следующее сообщение с помощью кнопок снизу:\n\n' \
                              + element.text.text

        return out

    else:
        out['message'] = 'Сейчас Бот отключен Администратором, пожалуйста повторите попытку позже.'
        out['button_text_list'] = ['Повторить попытку']

        return out
