from xml.etree import ElementTree
import os.path

from engine.xml_module.xml_element import XmlElement


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
