class XmlElement(object):
    """Элемент ветки дерева xml файла"""

    def __init__(self, element):
        """Конструктор"""
        self.element = element

        self.id = self.element.get('id')
        self.text = self.element.findall('text')[0]

        self.additions = self.element.findall('additions')[0]
        self.transitions = self.element.findall('transitions')[0]

        self.addition_list = self.additions.findall('addition')
        self.transition_list = self.transitions.findall('transition')