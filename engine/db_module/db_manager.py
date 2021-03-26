import sqlite3


class DbManager(object):
    """Работа с базой данных"""

    def __init__(self, db_full_file_path, table_name):
        """Конструктор (подключение к базе данных), выделение таблицы для работы с ней"""
        self.connection = sqlite3.connect(db_full_file_path)
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def add(self, user_id, element_id=-1):
        """Добавить новую запись в указанную таблицу базу данных"""
        sql_statement = "INSERT INTO `" + self.table_name + "` (`user_id`, `current_element_id`) VALUES(?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_id), str(element_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def remove(self, user_id):
        """Удалить запись из указанной таблицы базы данных"""
        sql_statement = "DELETE FROM `" + self.table_name + "` WHERE `user_id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def get_current_element_id(self, user_id):
        """Получить id вопроса по id пользователя"""
        sql_statement = "SELECT `current_element_id` FROM `" + self.table_name + "` WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(user_id),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                (r,) = result
                return r

    def get_all_user_id(self):
        """"""
        sql_statement = "SELECT `user_id` FROM `" + self.table_name + "`"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                out = []
                for r in result:
                    (_r,) = r
                    out += [_r]
                return out

    def update_current_element_id(self, user_id, element_id):
        """Обновить id вопроса по id пользователя"""
        sql_statement = "UPDATE `" + self.table_name + "` SET `current_element_id` = ? WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(element_id), str(user_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def disconnect(self):
        """Разорвать связь с базой данных"""
        self.connection.close()