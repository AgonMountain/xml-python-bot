from xml.etree import ElementTree
from data.config import XML_PATH


class XmlTreeManager(object):
    """
    Работа с ветками и элементами дерева xml файла
    > получить, создать, удалить ветку
    > получить из ветки, создать внутри ветки, удалить из ветки элемент
    """

    tree = ElementTree.parse(XML_PATH)
    root = tree.getroot()
    branch = None

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
            self.tree.write(XML_PATH, encoding='UTF-8')
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
            self.tree.write(XML_PATH, encoding='UTF-8')
            return True

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

        additions = ElementTree.SubElement(element, 'additions')
        transitions = ElementTree.SubElement(element, 'transitions')
        # создание списка additions [addition , addition , ...]
        for add in adds:
            attrib = {'branch_name': add['branch_name'], 'element_name': add['element_name']}
            addition = ElementTree.SubElement(additions, 'addition', attrib)
            addition.text = add['text']
        # создание списка transitions [transition , transition , ...]
        for tr in trs:
            attrib = {'branch_name': tr['branch_name'], 'next_element_name': tr['next_element_name']}
            transition = ElementTree.SubElement(transitions, 'transition', attrib)
            transition.text = tr['text']

        self.tree.write(XML_PATH, encoding='UTF-8')

    def delete_element(self, element):
        """
        Удалить элемент из активной ветки
        > element элемент
        > return
        """
        if (self.branch != None):
            self.branch.remove(element)
            self.tree.write(XML_PATH, encoding='UTF-8')
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
