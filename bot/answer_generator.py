from data.config import IDONTUNDERSTAND, XML_BRANCH_NAME_DEFAULT, XML_ELEMENT_NAME_DEFAULT


def generate(DB, XML, user_id, message_text):
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

    '''актуальные данные пользователя'''
    current = DB.get(user_id)
    current_branch_name = current['current_branch_name']
    current_element_name = current['current_element_name']

    '''нет пользователя в бд -> создаем его и задаем значение по умолчанию'''
    if current_element_name == None:
        DB.add(user_id, XML_BRANCH_NAME_DEFAULT, XML_ELEMENT_NAME_DEFAULT)

        current = DB.get(user_id)
        current_branch_name = current['current_branch_name']
        current_element_name = current['current_element_name']

        XML.switch_branch(current_branch_name)
        element = XML.get_element(current_element_name)
        out['message'] = element.text.text
        stop_loop_flag = True
    else:
        XML.switch_branch(current_branch_name)
        element = XML.get_element(current_element_name)

    '''списки текстов переходов и текстов дополнений'''
    transition_list = element.transition_list
    addition_list = element.addition_list

    '''поиск совпадения: сообщение от пользователя == текст перехода'''
    if not stop_loop_flag:
        for transition in transition_list:
            if message_text == transition.text:

                next_branch_name = transition.get('branch_name')
                next_element_name = transition.get('next_element_name')
                DB.update(user_id, next_branch_name, next_element_name)

                XML.switch_branch(next_branch_name)
                element = XML.get_element(next_element_name)
                out['message'] = element.text.text

                transition_list = element.transition_list
                addition_list = element.addition_list

                stop_loop_flag = True
                break

    '''поиск совпадения: сообщение от пользователя == текст дополнения'''
    if not stop_loop_flag:
        for addition in addition_list:
            if message_text == addition.text:

                branch_name = addition.get('branch_name')
                element_name = addition.get('element_name')

                XML.switch_branch(branch_name)
                element = XML.get_element(element_name)
                out['message'] = element.text.text

                stop_loop_flag = True
                break

    transition_text_list = [transition.text for transition in transition_list]
    addition_text_list = [addition.text for addition in addition_list]
    out['button_text_list'] = transition_text_list + addition_text_list

    return out
