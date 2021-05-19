from engine.xml_manager import XmlTreeManager
from engine.db_manager import DbManager
from data.config import DB_PATH, XML_PATH

class Convertor():

    @staticmethod
    def convert_from_xml_to_db():
        DB = DbManager(DB_PATH)
        XML = XmlTreeManager(XML_PATH)

        schemes = XML.get_all_schemes()

        for scheme in schemes:
            scheme_name = scheme['scheme_name']
            DB.add_scheme(scheme_name)
            scheme_data = DB.get_scheme_data(scheme_name)

            XML.switch_scheme(scheme_name)
            elements = XML.get_all_elements()

            for element in elements:
                element_name = element['element_name']
                DB.add_element(element_name, element['element_text'], scheme_data['id'])
                element_data = DB.get_element_data(element_name)

                # Сначала добавляем все элементы - потом связи между ними!
                # additions = XML.get_all_additions(element['element'])
                # for addition in additions:
                #     addition_name = addition['addition_name']
                #     DB.add_addition(element_data['id'], addition['addition_element'], )


        [DB.add_scheme(scheme['scheme_name']) for scheme in schemes]




    @staticmethod
    def clean_db(self):
        pass

    @staticmethod
    def clean_xml(self):
        pass


if __name__ == '__main__':
    Convertor.convert_from_xml_to_db()