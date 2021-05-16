import sqlite3
from engine.xml_manager import XmlTree
from data.config import XML_PATH, DB_PATH, DB_ADMIN_TABLE_NAME

class Admin(object):
    """
    Работа с админами и их возможностями
    """

    def __init__(self):
        """
        Конструктор
        """
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.table_name = DB_ADMIN_TABLE_NAME

        self.xml_manager = XmlTree(XML_PATH)

    @staticmethod
    def login(self, email, password):
        """
        Получить имя ветки и имя элемента
        > user_id идентификатор пользователя
        """
        sql_statement = "SELECT `password` FROM `" + self.table_name + "` WHERE `email` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(email),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                if result == password:
                    r = True
                else:
                    r = False
                return r

    def disconnect(self):
        """
        Разорвать связь с базой данных
        """
        self.connection.close()

    def create_branch(self, name):
        self.xml_manager.create_branch(name)

    def delete_branch(self, name):
        self.xml_manager.switch_branch(name)
        self.xml_manager.delete_branch()

    def update_branch(self, name, update):
        self.xml_manager.switch_branch(name)
        self.xml_manager.update_branch(update)
