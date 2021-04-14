class XmlElement(object):
    """Элемент ветки дерева xml файла"""

    def __init__(self, element):
        """Конструктор"""
        self.id = element.get('name')
        self.text = element.findall('text')[0]

        self.addition_list = element.findall('additions')[0].findall('addition')
        self.transition_list = element.findall('transitions')[0].findall('transition')