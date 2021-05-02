from data.config import IDONTUNDERSTAND


def generate(DB, XML, user_id, message_text):
    """
    Сформировать ответ для пользователя
    > db база данных пользователей, где хранятся данные рассматриваемого пользователя
    > message сообщение от пользователя
    return out ответное сообщение out['message'] и список слов для кнопок out['button_text_list']
    """
    out = {'message': None, 'button_text_list': None}
    out['message'] = IDONTUNDERSTAND
    stop_loop_flag = False  # незачем крутить циклы впустую

    current_element_id = DB.get_current_element_id(user_id)
    element = XML.get_element_by_id(current_element_id)

    '''нет пользователя в бд -> создаем его и задаем значение -1 (приветствие)'''
    if current_element_id == None:
        DB.add(user_id)
        current_element_id = DB.get_current_element_id(user_id)
        element = XML.get_element_by_id(current_element_id)
        out['message'] = element.text.text
        stop_loop_flag = True

    transition_list = element.transition_list
    addition_list = element.addition_list

    '''поиск совпадения: сообщение от пользователя == текст перехода'''
    if not stop_loop_flag:
        for transition in transition_list:
            if message_text == transition.text:

                next_element_id = transition.get('next_element_name')
                DB.update_current_element_id(user_id, next_element_id)

                element = XML.get_element_by_id(next_element_id)
                out['message'] = XML.get_element_by_id(next_element_id).text.text

                transition_list = element.transition_list
                addition_list = element.addition_list

                stop_loop_flag = True
                break

    '''поиск совпадения: сообщение от пользователя == текст дополнения'''
    if not stop_loop_flag:
        for addition in addition_list:
            if message_text == addition.text:

                element_id = addition.get('element_name')
                out['message'] = XML.get_element_by_id(element_id).text.text

                stop_loop_flag = True
                break

    transition_text_list = [transition.text for transition in transition_list]
    addition_text_list = [addition.text for addition in addition_list]
    out['button_text_list'] = transition_text_list + addition_text_list

    return out
