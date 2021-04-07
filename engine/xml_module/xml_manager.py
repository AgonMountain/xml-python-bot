from xml.etree import ElementTree
import os.path

from data.config import XML_PATH

from engine.xml_module.xml_element import XmlElement

tree = ElementTree.parse(XML_PATH)
root = tree.getroot()


class XmlTreeManager(object):
    """
    Работа с деревом xml файла
    > создание веток
    > удаление веток
    > переключение веток
    >
    >
    """
    def create_branch(self, branch_name):
        attrib = {'branch_name': branch_name}
        branch = root.makeelement('branch', attrib)
        root.append(branch)
        tree.write(XML_PATH, encoding='UTF-8')
        return None

    def delete_branch(self, branch_name):
        attrib = {'branch_name': branch_name}
        branch = root.find('branch').getiterator(attrib)
        root.remove(branch)
        tree.write(XML_PATH, encoding='UTF-8')
        return None

    def switch_branch(self, branch_name):
        return None

    def add_element(self, element):
        return None


if __name__ == '__main__':
    a = XmlTreeManager()
    a.delete_branch('test_21743')



class XmlManager(object):
    """Работа с xml файлом"""

    def __init__(self, xml_full_file_path, root_name, elements_name):
        """Конструктор"""
        self.tree = ElementTree.parse(os.path.abspath(os.path.join(xml_full_file_path)))
        self.root = self.tree.getroot()

        self.root = self.root.find(root_name)
        self.elements = self.root.findall(elements_name)

        self.elements = [XmlElement(element) for element in self.elements]

    def get_element_by_id(self, element_id_int):
        """Получить элемент по id из списка элементов"""
        for element in self.elements:
            if str(element.id) == str(element_id_int):
                return element