from xml.etree import ElementTree
from data.config import XML_PATH

class XmlElement(object):
    """
    Элемент ветки дерева xml файла
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
    Работа с ветками и элементами дерева xml файла
    > получить, создать, удалить ветку
    > получить из ветки, создать внутри ветки, удалить из ветки элемент
    """

    def __init__(self, XML_PATH):
        self.XML_PATH = XML_PATH
        self.tree = ElementTree.parse(self.XML_PATH)
        self.root = self.tree.getroot()
        self.branch = None

    """ Работа с ветками: получить, создать, сменить, обновить, удалить """

    def get_branch(self, name):
        """
        Получить ветку
        > name имя ветки
        > return
        """
        branches = self.root.findall('branch')
        for branch in branches:
            if str(branch.get('name')) == str(name):
                return branch
        return None

    def create_branch(self, name):
        """
        Создать новую ветку
        > name уникальное имя новой ветки
        > return
        """
        if (self.get_branch(name) != None):
            return False
        else:
            attrib = {'name': name}
            branch = self.root.makeelement('branch', attrib)
            self.root.append(branch)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            self.switch_branch(name)
            return True

    def switch_branch(self, name):
        """
        Сменить активную ветку
        """
        self.branch = self.get_branch(name)
        if (self.branch == None):
            return False
        else:
            return True

    def update_branch(self, name):
        """
        Редактировать ветку
        """
        if (self.get_branch(name) != None):
            return False
        else:
            self.branch.set('name', name)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    def delete_branch(self):
        """
        Удалить ветку
        > name уникальное имя существующей ветки
        > return
        """
        if (self.branch == None):
            return False
        else:
            self.root.remove(self.branch)
            self.branch = None
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    """ Работа с элементами: получить, создать, обновить, удалить, конвертировать"""

    def get_element(self, name):
        """
        Получить элемент из активной ветки по имени элемента
        > name имя элемента
        > return
        """
        elements = self.branch.findall('element')
        for element in elements:
            if str(element.get('name')) == str(name):
                return element
        return None

    def create_element(self, name, txt, adds, trs):
        """
        Создать элемент внутри ветки
        > branch ветка
        > name имя элемента
        > txt текст элемента
        > adds дополнения в виде списка словарей ([{'branch_name':'*имя ветки*', 'element_name':'*имя элемента*'}, ...])
        > trs переходы в виде списка словарей ([{'branch_name':'*имя ветки*', 'next_element_name':'*имя элемента*'}, ...])
        > return
        """
        attrib = {'name': name}
        element = ElementTree.SubElement(self.branch, 'element', attrib)

        text = ElementTree.SubElement(element, 'text')
        text.text = txt

        # additions = ElementTree.SubElement(element, 'additions')
        # transitions = ElementTree.SubElement(element, 'transitions')
        # # создание списка additions [addition , addition , ...]
        # for add in adds:
        #     attrib = {'branch_name': add['branch_name'], 'element_name': add['element_name']}
        #     addition = ElementTree.SubElement(additions, 'addition', attrib)
        #     addition.text = add['text']
        # # создание списка transitions [transition , transition , ...]
        # for tr in trs:
        #     attrib = {'branch_name': tr['branch_name'], 'next_element_name': tr['next_element_name']}
        #     transition = ElementTree.SubElement(transitions, 'transition', attrib)
        #     transition.text = tr['text']

        self.tree.write(self.XML_PATH, encoding='UTF-8')

    def udpate_element(self, element):
        """TODO"""

    def delete_element(self, element):
        """
        Удалить элемент из активной ветки
        > element элемент
        > return
        """
        if (self.branch != None):
            self.branch.remove(element)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True
        else:
            return False

    def convert(self, element):
        """
        Конвертировать element в удобный для использования формат XmlElement
        > element элемент для конвертации
        > return
        """
        return XmlElement(element)

    """ Работа с атрибутами: получить, создать, обновить, удалить """

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

    def create_addition(self, element, branch_name, element_name, addition_text):
        """
        Создать дополнение внутри элемента
        > element - элемент ветки, к которому нужно создать дополнение
        > branch_name - имя ветки, на элемент который необходимо сделать переход
        > element_name - имя элемента, который будет служить дополнением
        > addition_text - условие дополнения
        > return - True - если дополнение создано, иначе False
        """
        additions = element.findall('additions')[0]

        '''Проверка на повторение текста'''
        for addition in additions:
            if str(addition.text) == str(addition_text):
                return False

        attrib = {'branch_name': branch_name, 'element_name': element_name}
        addition = ElementTree.SubElement(additions, 'addition', attrib)
        addition.text = addition_text

        self.tree.write(self.XML_PATH, encoding='UTF-8')
        return True

    def update_addition(self, element, old_addition_text, new_branch_name, new_element_name, new_addition_text):
        """
        Обновить дополнение внутри элемента
        > element - элемент ветки, к которому нужно создать дополнение
        > old_addition_text - старый текст дополненения
        > new_branch_name - имя ветки, на элемент который необходимо сделать переход
        > new_element_name - имя элемента, который будет служить дополнением
        > new_addition_text - текст / условие дополнения
        > return - True - если дополнение обновлено, иначе False
        """
        additions = element.findall('additions')[0]

        '''Проверка на существование дополнения'''
        for addition in additions:
            if addition.text == old_addition_text:
                addition.set('branch_name', new_branch_name)
                addition.set('element_name', new_element_name)
                addition.text = new_addition_text
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False

    def delete_addition(self, element, addition_text):
        """
        Удалить дополнение внутри элемента
        > element - элемент, дополнение которого нужно удалить
        > addition_text - текст / условие дополнения
        > return - True - если дополнение удалено, иначе False
        """
        additions = element.findall('additions')[0]

        '''Проверка на существование дополнения'''
        for addition in additions:
            if addition.text == addition_text:
                additions.remove(addition)
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False

    """ Работа с переходами: получить, создать, обновить, удалить """

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

    def create_transition(self, element, branch_name, next_element_name, transition_text):
        """
        Создать переход внутри элемента
        > element - элемент ветки, к которому нужно создать дополнение
        > branch_name - имя ветки, на элемент который необходимо сделать переход
        > next_element_name - имя элемента, на который будет выполнен переход
        > transition_text - текст / условие перехода
        > return - True - если переход создан, иначе False
        """
        transitions = element.findall('transitions')[0]

        '''Проверка на повторение текста'''
        for transition in transitions:
            if str(transition.text) == str(transition_text):
                return False

        attrib = {'branch_name': branch_name, 'next_element_name': next_element_name}
        transition = ElementTree.SubElement(transitions, 'transition', attrib)
        transition.text = transition_text

        self.tree.write(self.XML_PATH, encoding='UTF-8')
        return True

    def update_transition(self, element, old_transition_text, new_branch_name, new_next_element_name, new_transition_text):
        """
        Обновить переход внутри элемента
        > element - элемент ветки, к которому нужно создать переход
        > old_transition_text - старый текст / условие перехода
        > new_branch_name - имя ветки, на элемент который необходимо сделать переход
        > new_next_element_name - имя элемента, на который необходимо сделать переход
        > new_transition_text - новый текст / условие перехода
        > return - True - если дополнение обновлено, иначе False
        """
        transitions = element.findall('transitions')[0]

        '''Проверка на существование перехода'''
        for transition in transitions:
            if transition.text == old_transition_text:
                transition.set('branch_name', new_branch_name)
                transition.set('next_element_name', new_next_element_name)
                transition.text = new_transition_text
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False

    def delete_transition(self, element, transition_text):
        """
        Удалить переход внутри элемента
        > element - элемент, переход которого нужно удалить
        > transition_text - текст / условие перехода
        > return - True - если переход удален, иначе False
        """
        transitions = element.findall('transitions')[0]

        '''Проверка на существование перехода'''
        for transition in transitions:
            if transition.text == transition_text:
                transitions.remove(transition)
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False


""" Ручное тестирование ): """
if __name__ == "__main__":
    tree = XmlTree(XML_PATH)
    tree.switch_branch('Приверженность')

    el = tree.get_element('-1')

    tree.delete_transition(el, 'Переход2')