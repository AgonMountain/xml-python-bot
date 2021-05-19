from xml.etree import ElementTree

class XmlElement(object):
    """
    Элемент схемы дерева xml файла
    """

    def __init__(self, element):
        """
        Конструктор
        """
        self.element = element

        self.name = self.element.get('name')
        self.text = self.element.findall('text')[0]

        self.additions = self.element.findall('additions')[0]
        self.transitions = self.element.findall('transitions')[0]

        self.addition_list = self.additions.findall('addition')
        self.transition_list = self.transitions.findall('transition')

class XmlTreeManager(object):
    """
    Работа с схемами, элементами и компонентами элементов дерева xml файла
    """

    def __init__(self, XML_PATH):
        self.XML_PATH = XML_PATH
        self.tree = ElementTree.parse(self.XML_PATH)
        self.root = self.tree.getroot()
        self.scheme = None

    """ Работа с схемами """
    def get_all_schemes(self):
        """
        Получить все схемы
        @return [ {'original', 'name'} ]
        """
        schemes = self.root.findall('scheme')
        schemes = [{'original': scheme,
                    'name': scheme.get('name')}
                   for scheme in schemes]
        return schemes
    def get_scheme(self, name):
        """
        Получить схему
        @param  name имя схемы
        @return схема, если таковая найдена, иначе None
        """
        schemes = self.root.findall('scheme')
        for scheme in schemes:
            if str(scheme.get('name')) == str(name):
                return scheme
        return None
    def create_scheme(self, name):
        """
        Создать новую схему
        @param name имя новой схемы (должно быть уникальным)
        @return True если схема была создана, иначе False
        """
        '''проверка на повторение'''
        if self.get_scheme(name) != None:
            return False
        else:
            attrib = {'name': name}
            scheme = self.root.makeelement('scheme', attrib)
            self.root.append(scheme)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def switch_scheme(self, name):
        """
        Сменить *активную схему* (для работы с ней и ее элементами)
        @param name имя схемы, которую нужно сделать активной
        @return True если *активная схема* была изменена, иначе False
        """
        scheme = self.get_scheme(name)
        '''проверка на существование'''
        if scheme != None:
            self.scheme = scheme
            return True
        else:
            return False
    def update_scheme(self, new_name):
        """
        Редактировать имя схемы
        @param new_name новое имя схемы (должно быть уникальным)
        @return True если схема была обновлена, иначе False
        """
        '''проверка на повторение'''
        if self.get_scheme(new_name) != None:
            return False
        else:
            self.scheme.set('name', new_name)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def delete_scheme(self):
        """
        Удалить *активную схему*
        @return True если схема была удалена, иначе False (когда нет *активной схемы*)
        @param self.scheme если схема была удалена, значение поля будет равным None
        """
        if self.scheme == None:
            return False
        else:
            self.root.remove(self.scheme)
            self.scheme = None
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    """ Работа с элементами """
    def get_all_elements(self):
        """
        Получить все элементы *активной ветки*
        @return [ {'original', 'name', 'text', 'scheme_name'} ]
        """
        elements = self.scheme.findall('element')
        elements = [{'original': element,
                     'name': element.get('name'),
                     'text': element.findall('text')[0].text,
                     'scheme_name': self.scheme.get('name')}
                    for element in elements]
        return elements
    def get_element(self, name):
        """
        Получить элемент из *активной схемы*
        @param name имя элемента
        @return элемент если он был найден, иначе None
        """
        if self.scheme != None:
            elements = self.scheme.findall('element')
            for element in elements:
                if str(element.get('name')) == str(name):
                    return element
        return None
    def create_element(self, name, text):
        """
        Создать элемент внутри *активной схемы*
        @param name имя элемента (должно быть уникальным)
        @param text текст элемента
        @return True если элемент был создан, иначе False
        """
        if self.scheme != None:
            if self.get_element(name) == None:
                attrib = {'name': name}
                element = ElementTree.SubElement(self.scheme, 'element', attrib)
                etext = ElementTree.SubElement(element, 'text')
                etext.text = text
                ElementTree.SubElement(element, 'additions')
                ElementTree.SubElement(element, 'transitions')
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def update_element(self, old_name, new_name, new_text):
        """
        Обновить элемент внутри *активной схемы*
        @param old_name старое имя элемента (по нему идет поиск)
        @param new_name новое имя элемента
        @param new_text новый текст внутри элемента
        @return True если элемент был обновлен, иначе False
        """
        if self.scheme != None:
            element = self.get_element(old_name)
            if element != None:
                element.set('name', new_name)
                element.text = new_text
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def delete_element(self, name):
        """
        Удалить элемент из *активной схемы*
        @param name имя элемента
        @return True если элемент был удален, иначе False
        """
        if self.scheme != None:
            element = self.get_element(name)
            if element != None:
                self.scheme.remove(element)
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False
    def convert_element(self, element):
        """
        Конвертировать element (xml объект) в формат XmlElement
        @param element элемент для конвертации
        @return конвертированный элемент
        """
        return XmlElement(element)

    """ Работа с дополнениями """
    def get_all_additions(self, element):
        """
        Получить все дополнения элемента
        @param element элемент
        @return [ {'original', 'base_element_name', 'text', 'addition_scheme_name', 'addition_element_name'} ]
        """
        additions = element.findall('additions')[0]
        additions = additions.findall('addition')
        additions = [{'original': addition,
                      'base_element_name': element.get('name'),
                      'text': addition.text,
                      'addition_scheme_name': addition.get('scheme_name'),
                      'addition_element_name': addition.get('element_name')}
                     for addition in additions]
        return additions
    def get_addition(self, element, text):
        """
        Получить дополнение элемента
        @param element элемент
        @param text текст / условие дополнения
        @return дополнение если оно было найдено, иначе None
        """
        additions = element.findall('additions')[0]

        for addition in additions:
            if str(addition.text) == str(text):
                return addition
        return None
    def create_addition(self, element, addition_scheme_name, addition_element_name, text):
        """
        Создать дополнение внутри элемента
        @param element элемент схемы, к которому нужно создать дополнение
        @param addition_scheme_name имя схемы, на элемент который необходимо сделать переход
        @param addition_element_name имя элемента, который будет служить дополнением
        @param text условие дополнения
        @return True если дополнение создано, иначе False
        """
        additions = element.findall('additions')[0]

        '''проверка на повторение'''
        if self.get_addition(element, text) != None:
            return False
        else:
            attrib = {'scheme_name': addition_scheme_name, 'element_name': addition_element_name}
            addition = ElementTree.SubElement(additions, 'addition', attrib)
            addition.text = text

            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def update_addition(self, element, old_text, new_addition_scheme_name, new_addition_element_name, new_text):
        """
        Обновить дополнение внутри элемента
        @param element элемент схемы, к которому нужно создать дополнение
        @param old_text старый текст дополненения
        @param new_addition_scheme_name имя схемы, на элемент который необходимо сделать переход
        @param new_addition_element_name имя элемента, который будет служить дополнением
        @param new_text текст / условие дополнения
        @return True если дополнение обновлено, иначе False
        """
        addition = self.get_addition(element, old_text)

        '''проверка на существование'''
        if addition != None:
            addition.set('scheme_name', new_addition_scheme_name)
            addition.set('element_name', new_addition_element_name)
            addition.text = new_text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False
    def delete_addition(self, element, text):
        """
        Удалить дополнение внутри элемента
        @param element элемент, дополнение которого нужно удалить
        @param text текст / условие дополнения
        @return True если дополнение удалено, иначе False
        """
        additions = element.findall('additions')[0]
        addition = self.get_addition(element, text)

        '''проверка на существование'''
        if addition != None:
            additions.remove(addition)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False

    """ Работа с переходами """
    def get_all_transitions(self, element):
        """
        Получить все переходы элемента
        @param element элемент
        @return [ {'original', 'base_element_name', 'text', 'scheme_name', 'element_name'} ]
        """
        transitions = element.findall('transitions')[0]
        transitions = transitions.findall('transition')
        transitions = [{'original': transition,
                        'base_element_name': element.get('name'),
                        'text': transition.text,
                        'transition_scheme_name': transition.get('scheme_name'),
                        'transition_element_name': transition.get('element_name')}
                     for transition in transitions]
        return transitions
    def get_transition(self, element, text):
        """
        Получить переход элемента
        @param element элемент
        @param text текст / условие перехода
        @return переход если он был найден, иначе None
        """
        transitions = element.findall('transitions')[0]

        for transition in transitions:
            if str(transition.text) == str(text):
                return transition
        return None
    def create_transition(self, element, transition_scheme_name, transition_element_name, text):
        """
        Создать переход внутри элемента
        @param element элемент схемы, к которому нужно создать дополнение
        @param transition_scheme_name имя схемы, на элемент который необходимо сделать переход
        @param transition_element_name имя элемента, на который будет выполнен переход
        @param text текст / условие перехода
        @return True если переход создан, иначе False
        """
        transitions = element.findall('transitions')[0]

        '''проверка на повторение'''
        if self.get_transition(element, text) != None:
            return False
        else:
            attrib = {'scheme_name': transition_scheme_name, 'element_name': transition_element_name}
            transition = ElementTree.SubElement(transitions, 'transition', attrib)
            transition.text = text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
    def update_transition(self, element, old_text, new_transition_scheme_name, new_transition_element_name, new_text):
        """
        Обновить переход внутри элемента
        @param element элемент схемы, к которому нужно создать переход
        @param old_text старый текст / условие перехода
        @param new_transition_scheme_name имя схемы, на элемент который необходимо сделать переход
        @param new_transition_element_name имя элемента, на который необходимо сделать переход
        @param new_text новый текст / условие перехода
        @return True если дополнение обновлено, иначе False
        """
        transition = self.get_transition(element, old_text)

        '''проверка на существование'''
        if transition != None:
            transition.set('scheme_name', new_transition_scheme_name)
            transition.set('element_name', new_transition_element_name)
            transition.text = new_text
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False
    def delete_transition(self, element, text):
        """
        Удалить переход внутри элемента
        @param element элемент, переход которого нужно удалить
        @param text текст / условие перехода
        @return True если переход удален, иначе False
        """
        transitions = element.findall('transitions')[0]
        transition = self.get_transition(element, text)

        '''проверка на существование'''
        if transition != None:
            transitions.remove(transition)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False
