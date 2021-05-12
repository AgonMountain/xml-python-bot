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
    Работа с ветками, элементами и компонентами элементов дерева xml файла
    > Ветки: получить, создать, сменить, обновить, удалить
    > Элементы: получить, создать, обновить, удалить, конвертировать
    > Дополнения к элементу: получить, создать, обновить, удалить
    > Переходы к элементу: получить, создать, обновить, удалить
    """

    def __init__(self, XML_PATH):
        self.XML_PATH = XML_PATH
        self.tree = ElementTree.parse(self.XML_PATH)
        self.root = self.tree.getroot()
        self.branch = None

    """ Работа с ветками: получить, создать, сменить, обновить, удалить """

    def get_branch(self, branch_name):
        """
        Получить ветку
        > branch_name - имя ветки
        > return - ветка, если таковая найдена, иначе None
        """
        branches = self.root.findall('branch')
        for branch in branches:
            if str(branch.get('name')) == str(branch_name):
                return branch
        return None

    def create_branch(self, branch_name):
        """
        Создать новую ветку
        > branch_name - имя новой ветки (должно быть уникальным)
        > return - True - если ветка была создана, иначе False
        """
        '''проверка на повторение'''
        if self.get_branch(branch_name) != None:
            return False
        else:
            attrib = {'name': branch_name}
            branch = self.root.makeelement('branch', attrib)
            self.root.append(branch)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    def switch_branch(self, branch_name):
        """
        Сменить *активную ветку* (для работы с ней и ее элементами)
        > branch_name - имя ветки, которую нужно сделать активной
        > return - True - если *активная ветка* была изменена, иначе False
        """
        branch = self.get_branch(branch_name)
        '''проверка на существование'''
        if branch != None:
            self.branch = branch
            return True
        else:
            return False

    def update_branch(self, new_branch_name):
        """
        Редактировать имя ветки
        > new_branch_name - новое имя ветки (должно быть уникальным)
        > return - True - если ветка была обновлена, иначе False
        """
        '''проверка на повторение'''
        if self.get_branch(new_branch_name) != None:
            return False
        else:
            self.branch.set('name', new_branch_name)
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    def delete_branch(self):
        """
        Удалить *активную ветку*
        > return - True - если ветка была удалена, иначе False (когда нет *активной ветки*)
        > self.branch - если ветка была удалена, значение поля будет равным None
        """
        if self.branch == None:
            return False
        else:
            self.root.remove(self.branch)
            self.branch = None
            self.tree.write(self.XML_PATH, encoding='UTF-8')
            return True

    """ Работа с элементами: получить, создать, обновить, удалить, конвертировать"""

    def get_element(self, element_name):
        """
        Получить элемент из *активной ветки*
        > name - имя элемента
        > return - элемент - если он был найден, иначе None
        """
        if self.branch != None:
            elements = self.branch.findall('element')
            for element in elements:
                if str(element.get('name')) == str(element_name):
                    return element
        return None

    def create_element(self, element_name, element_text):
        """
        Создать элемент внутри *активной ветки*
        > element_name - имя элемента (должно быть уникальным)
        > element_text - текст элемента
        > return - True - если элемент был создан, иначе False
        """
        if self.branch != None:
            if self.get_element(element_name) == None:
                attrib = {'name': element_name}
                element = ElementTree.SubElement(self.branch, 'element', attrib)
                text = ElementTree.SubElement(element, 'text')
                text.text = element_text
                ElementTree.SubElement(element, 'additions')
                ElementTree.SubElement(element, 'transitions')
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False

    def update_element(self, old_element_name, new_element_name, new_element_text):
        """
        Обновить элемент внутри *активной ветки*
        > old_element_name - старое имя элемента (по нему идет поиск)
        > new_element_name - новое имя элемента
        > new_element_text - новый текст внутри элемента
        > return - True - если элемент был обновлен, иначе False
        """
        if self.branch != None:
            element = self.get_element(old_element_name)
            if element != None:
                element.set('name', new_element_name)
                element.text = new_element_text
                self.tree.write(self.XML_PATH, encoding='UTF-8')
                return True

        return False

    def delete_element(self, element_name):
        """
        Удалить элемент из *активной ветки*
        > element_name - имя элемента
        > return - True - если элемент был удален, иначе False
        """
        if self.branch != None:
            element = self.get_element(element_name)
            if element != None:
                self.branch.remove(element)
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

        '''проверка на повторение'''
        if self.get_addition(element, addition_text) != None:
            return False
        else:
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
        addition = self.get_addition(element, old_addition_text)

        '''проверка на существование'''
        if addition != None:
            addition.set('branch_name', new_branch_name)
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

        '''проверка на повторение'''
        if self.get_transition(element, transition_text) != None:
            return False
        else:
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
        transition = self.get_transition(element, old_transition_text)

        '''проверка на существование'''
        if transition != None:
            transition.set('branch_name', new_branch_name)
            transition.set('next_element_name', new_next_element_name)
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


""" Ручное тестирование ): """
if __name__ == "__main__":
    tree = XmlTree(XML_PATH)

    tree.create_branch('ветка')
    tree.switch_branch('ветка')
    tree.create_element('элемент', 'элемент_текст')

    el = tree.get_element('элемент')
    tree.create_addition(el, 'ветка1', 'элемент1', 'дополнение_текст')
    tree.create_transition(el, 'ветка2', 'элемент2', 'дополнение_текст')
