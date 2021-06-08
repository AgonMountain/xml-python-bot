from engine.xml_manager import XmlTreeManager
from engine.db_manager import DbManager


class Convertor():

    @staticmethod
    def convert_from_xml_to_db(XML_PATH, DB_PATH):
        """
        Перенести данные из xml файла в базу данных
        @param DB_PATH полный путь к базе данных
        @param XML_PATH полный путь к xml файлу
        """
        Convertor.clean_xml_reference_from_db(DB_PATH)
        DB = DbManager(DB_PATH)
        XML = XmlTreeManager(XML_PATH)

        schemes = XML.get_all_schemes()

        for scheme in schemes:
            scheme_id = DB.add_scheme(scheme['name'])

            XML.switch_scheme(scheme['name'])
            elements = XML.get_all_elements()

            for element in elements:
                DB.add_element(element['name'], element['text'], scheme_id)


            elements = DB.get_all_elements(scheme_id)
            # Сначала добавляем все элементы - потом связи между ними!
            for element in elements:
                xml_element = XML.get_element(element[1])

                additions = XML.get_all_additions(xml_element)
                for addition in additions:
                    addition_element_id = DB.get_element_id(addition['addition_element_name'])
                    DB.add_addition(element[0], addition_element_id, addition['text'])

                transitions = XML.get_all_transitions(xml_element)
                for transition in transitions:
                    transition_element_id = DB.get_element_id(transition['transition_element_name'])
                    DB.add_transition(element[0], transition_element_id, transition['text'])

    @staticmethod
    def convert_from_db_to_xml(DB_PATH, XML_PATH):
        """
        Перенести данные из базы данных в xml файл
        @param DB_PATH полный путь к базе данных
        @param XML_PATH полный путь к xml файлу
        """
        Convertor.clean_db_reference_from_xml(XML_PATH)
        DB = DbManager(DB_PATH)
        XML = XmlTreeManager(XML_PATH)

        schemes = DB.get_all_schemes()

        for scheme in schemes:
            XML.create_scheme(scheme[1])
            XML.switch_scheme(scheme[1])

            elements = DB.get_all_elements(scheme[0])

            # создаем все элементы в xml (без переходов и дополнений)
            for element in elements:
                XML.create_element(element[1], element[2])

            # ...
            elements = XML.get_all_elements()
            for element in elements:
                element_id = DB.get_element_id(element['name'])
                addition_id_list = DB.get_all_additions_id_from_element(element_id)
                transition_id_list = DB.get_all_transitions_id_from_element(element_id)

                for addition_id in addition_id_list:
                    addition_data = DB.get_addition_data(addition_id[0])

                    addition_element = DB.get_element_data(addition_data['addition_id'])
                    scheme_name = DB.get_scheme_data(addition_element['scheme_id'])['name']
                    XML.create_addition(element['original'], scheme_name, addition_element['name'], addition_data['text'])

                for transition_id in transition_id_list:
                    transition_data = DB.get_transition_data(transition_id[0])

                    transition_element = DB.get_element_data(transition_data['transition_id'])
                    scheme_name = DB.get_scheme_data(transition_element['scheme_id'])['name']
                    XML.create_transition(element['original'], scheme_name, transition_element['name'], transition_data['text'])

    @staticmethod
    def clean_xml_reference_from_db(DB_PATH):
        """
        Очистить базу данных от схем и элементов
        @param DB_PATH полный путь к базе данных с схемами и элементами
        """
        DB = DbManager(DB_PATH)

        DB.clean_table_addition()
        DB.clean_table_transition()
        DB.clean_table_element()
        DB.clean_table_scheme()

    @staticmethod
    def clean_db_reference_from_xml(XML_PATH):
        """
        Очистить файл xml от схем и элементов
        @param XML_PATH полный путь к xml файлу с схемами и элементами
        """
        XML = XmlTreeManager(XML_PATH)
        schemes = XML.get_all_schemes()
        for scheme in schemes:
            XML.switch_scheme(scheme['name'])
            XML.delete_scheme()
