from xml.etree import ElementTree
from data.config import XML_PATH

class XmlElement(object):
    """
    Элемент схемы дерева xml файла
    """

    def __init__(self, element):
        """
        Конструктор
        """
        self.element = element

        self.id = self.element.get('name')
        self.text = self.element.findall('text')[0]

        self.additions = self.element.findall('additions')[0]
        self.transitions = self.element.findall('transitions')[0]

        self.addition_list = self.additions.findall('addition')
        self.transition_list = self.transitions.findall('transition')

class XmlTree(object):
    """
    Работа с схемами, элементами и компонентами элементов дерева xml файла
    > схемы: получить, создать, сменить, обновить, удалить
    > Элементы: получить, создать, обновить, удалить, конвертировать
    > Дополнения к элементу: получить, создать, обновить, удалить
    > Переходы к элементу: получить, создать, обновить, удалить
    """

    def __init__(self, XML_PATH):
        self.XML_PATH = XML_PATH
        self.tree = ElementTree.parse(self.XML_PATH)
        self.root = self.tree.getroot()
        self.scheme = None

    """ Работа с схемами: получить, создать, сменить, обновить, удалить """
    def get_all_schemes(self):
        """
        """
        schemes = self.root.findall('scheme')
        schemes = [{'scheme_name': scheme.get('name')}
                   for scheme in schemes]
        return schemes
    def get_scheme(self, scheme_name):
        """
        Получить схему
        > scheme_name - имя схемы
        > return - схема, если таковая найдена, иначе None
        """
        schemes = self.root.findall('scheme')
        for scheme in schemes:
            if str(scheme.get('name')) == str(scheme_name):
                return scheme
        return None
    def create_scheme(self, scheme_name):
        """
        Создать новую схему
        > scheme_name - имя новой схемы (должно быть уникальным)
        > return - True - если схема была создана, иначе False
        """
        '''проверка на повторение'''
        if self.get_scheme(scheme_name) != None:
            return False
        else:
            attrib = {'name': scheme_name}
            scheme = self.root.makeelement('scheme', attrib)
            self.root.append(scheme)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def switch_scheme(self, scheme_name):
        """
        Сменить *активную схему* (для работы с ней и ее элементами)
        > scheme_name - имя схемы, которую нужно сделать активной
        > return - True - если *активная схема* была изменена, иначе False
        """
        scheme = self.get_scheme(scheme_name)
        '''проверка на существование'''
        if scheme != None:
            self.scheme = scheme
            return True
        else:
            return False
    def update_scheme(self, new_scheme_name):
        """
        Редактировать имя схемы
        > new_scheme_name - новое имя схемы (должно быть уникальным)
        > return - True - если схема была обновлена, иначе False
        """
        '''проверка на повторение'''
        if self.get_scheme(new_scheme_name) != None:
            return False
        else:
            self.scheme.set('name', new_scheme_name)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def delete_scheme(self):
        """
        Удалить *активную схему*
        > return - True - если схема была удалена, иначе False (когда нет *активной схемы*)
        > self.scheme - если схема была удалена, значение поля будет равным None
        """
        if self.scheme == None:
            return False
        else:
            self.root.remove(self.scheme)
            self.scheme = None
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    """ Работа с элементами: получить, создать, обновить, удалить, конвертировать"""

    def get_all_elements(self):
        """
        """
        elements = self.scheme.findall('element')
        elements = [{'element_name': element.get('name'),
                     'element_text': element.findall('text')[0].text,
                     'scheme_name': self.scheme.get('name')}
                    for element in elements]
        return elements
    def get_element(self, element_name):
        """
        Получить элемент из *активной схемы*
        > name - имя элемента
        > return - элемент - если он был найден, иначе None
        """
        if self.scheme != None:
            elements = self.scheme.findall('element')
            for element in elements:
                if str(element.get('name')) == str(element_name):
                    return element
        return None
    def create_element(self, element_name, element_text):
        """
        Создать элемент внутри *активной схемы*
        > element_name - имя элемента (должно быть уникальным)
        > element_text - текст элемента
        > return - True - если элемент был создан, иначе False
        """
        if self.scheme != None:
            if self.get_element(element_name) == None:
                attrib = {'name': element_name}
                element = ElementTree.SubElement(self.scheme, 'element', attrib)
                text = ElementTree.SubElement(element, 'text')
                text.text = element_text
                ElementTree.SubElement(element, 'additions')
                ElementTree.SubElement(element, 'transitions')
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def update_element(self, old_element_name, new_element_name, new_element_text):
        """
        Обновить элемент внутри *активной схемы*
        > old_element_name - старое имя элемента (по нему идет поиск)
        > new_element_name - новое имя элемента
        > new_element_text - новый текст внутри элемента
        > return - True - если элемент был обновлен, иначе False
        """
        if self.scheme != None:
            element = self.get_element(old_element_name)
            if element != None:
                element.set('name', new_element_name)
                element.text = new_element_text
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def delete_element(self, element_name):
        """
        Удалить элемент из *активной схемы*
        > element_name - имя элемента
        > return - True - если элемент был удален, иначе False
        """
        if self.scheme != None:
            element = self.get_element(element_name)
            if element != None:
                self.scheme.remove(element)
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def convert_element(self, element):
        """
        Конвертировать element (xml объект) в формат XmlElement
        > element - элемент для конвертации
        > return - конвертированный элемент
        """
        return XmlElement(element)

    """ Работа с дополнениями: получить, создать, обновить, удалить """

    def get_all_additions(self, element):
        """
        """
        additions = element.findall('additions')[0]
        additions = additions.findall('addition')
        additions = [{'element_name': element.get('name'),
                      'addition_text': addition.text,
                      'addition_scheme_name': addition.get('scheme_name'),
                      'addition_element_name': addition.get('element_name')}
                     for addition in additions]
        return additions
    def get_addition(self, element, addition_text):
        """
        Получить дополнение элемента
        > element - элемент
        > addition_text - текст / условие дополнения
        > return - дополнение - если оно было найдено, иначе None
        """
        additions = element.findall('additions')[0]

        for addition in additions:
            if str(addition.text) == str(addition_text):
                return addition
        return None
    def create_addition(self, element, scheme_name, element_name, addition_text):
        """
        Создать дополнение внутри элемента
        > element - элемент схемы, к которому нужно создать дополнение
        > scheme_name - имя схемы, на элемент который необходимо сделать переход
        > element_name - имя элемента, который будет служить дополнением
        > addition_text - условие дополнения
        > return - True - если дополнение создано, иначе False
        """
        additions = element.findall('additions')[0]

        '''проверка на повторение'''
        if self.get_addition(element, addition_text) != None:
            return False
        else:
            attrib = {'scheme_name': scheme_name, 'element_name': element_name}
            addition = ElementTree.SubElement(additions, 'addition', attrib)
            addition.text = addition_text

            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def update_addition(self, element, old_addition_text, new_scheme_name, new_element_name, new_addition_text):
        """
        Обновить дополнение внутри элемента
        > element - элемент схемы, к которому нужно создать дополнение
        > old_addition_text - старый текст дополненения
        > new_scheme_name - имя схемы, на элемент который необходимо сделать переход
        > new_element_name - имя элемента, который будет служить дополнением
        > new_addition_text - текст / условие дополнения
        > return - True - если дополнение обновлено, иначе False
        """
        addition = self.get_addition(element, old_addition_text)

        '''проверка на существование'''
        if addition != None:
            addition.set('scheme_name', new_scheme_name)
            addition.set('element_name', new_element_name)
            addition.text = new_addition_text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False
    def delete_addition(self, element, addition_text):
        """
        Удалить дополнение внутри элемента
        > element - элемент, дополнение которого нужно удалить
        > addition_text - текст / условие дополнения
        > return - True - если дополнение удалено, иначе False
        """
        additions = element.findall('additions')[0]
        addition = self.get_addition(element, addition_text)

        '''проверка на существование'''
        if addition != None:
            additions.remove(addition)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False

    """ Работа с переходами: получить, создать, обновить, удалить """

    def get_all_transitions(self, element):
        """
        """
        transitions = element.findall('transitions')[0]
        transitions = transitions.findall('transition')
        transitions = [{'element_name': element.get('name'),
                      'transition_text': transition.text,
                      'transition_scheme_name': transition.get('scheme_name'),
                      'transition_element_name': transition.get('element_name')}
                     for transition in transitions]
        return transitions
    def get_transition(self, element, transition_text):
        """
        Получить переход элемента
        > element - элемент
        > transition_text - текст / условие перехода
        > return - переход - если он был найден, иначе None
        """
        transitions = element.findall('transitions')[0]

        for transition in transitions:
            if str(transition.text) == str(transition_text):
                return transition
        return None
    def create_transition(self, element, scheme_name, element_name, transition_text):
        """
        Создать переход внутри элемента
        > element - элемент схемы, к которому нужно создать дополнение
        > scheme_name - имя схемы, на элемент который необходимо сделать переход
        > element_name - имя элемента, на который будет выполнен переход
        > transition_text - текст / условие перехода
        > return - True - если переход создан, иначе False
        """
        transitions = element.findall('transitions')[0]

        '''проверка на повторение'''
        if self.get_transition(element, transition_text) != None:
            return False
        else:
            attrib = {'scheme_name': scheme_name, 'element_name': element_name}
            transition = ElementTree.SubElement(transitions, 'transition', attrib)
            transition.text = transition_text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def update_transition(self, element, old_transition_text, new_scheme_name, new_element_name, new_transition_text):
        """
        Обновить переход внутри элемента
        > element - элемент схемы, к которому нужно создать переход
        > old_transition_text - старый текст / условие перехода
        > new_scheme_name - имя схемы, на элемент который необходимо сделать переход
        > new_element_name - имя элемента, на который необходимо сделать переход
        > new_transition_text - новый текст / условие перехода
        > return - True - если дополнение обновлено, иначе False
        """
        transition = self.get_transition(element, old_transition_text)

        '''проверка на существование'''
        if transition != None:
            transition.set('scheme_name', new_scheme_name)
            transition.set('element_name', new_element_name)
            transition.text = new_transition_text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False
    def delete_transition(self, element, transition_text):
        """
        Удалить переход внутри элемента
        > element - элемент, переход которого нужно удалить
        > transition_text - текст / условие перехода
        > return - True - если переход удален, иначе False
        """
        transitions = element.findall('transitions')[0]
        transition = self.get_transition(element, transition_text)

        '''проверка на существование'''
        if transition != None:
            transitions.remove(transition)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False


    def transfer_from_xml_to_db(self):
        pass



""" Ручное тестирование ): """
if __name__ == "__main__":
    tree = XmlTree(XML_PATH)
    tree.switch_scheme('Приверженность')
    element = tree.get_element('2')
    print(tree.get_all_additions(element))

