import sqlite3


class DbManager(object):
    """
    Работа с базой данных
    """

    def __init__(self, db_full_file_path, table_name):
        """
        Конструктор (подключение к базе данных), выделение таблицы для работы с ней
        > db_full_file_path полный путь к базе данных
        > table_name имя таблицы
        """
        self.connection = sqlite3.connect(db_full_file_path)
        self.cursor = self.connection.cursor()
        self.table_name = table_name

    def add(self, user_id, branch_name, element_name):
        """
        Добавить нового пользователя в базу данных
        > user_id идентификатор пользователя
        > branch_name имя ветки
        > element_name имя элемента
        """
        sql_statement = "INSERT INTO `" + self.table_name + "` (`user_id`, `current_branch_name`, `current_element_name`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_id), str(branch_name), str(element_name)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def update(self, user_id, branch_name, element_name):
        """
        Обновить данные пользователя в базе данных
        > user_id идентификатор пользователя
        > branch_name имя ветки
        > element_name имя элемента
        """
        sql_statement = "UPDATE `" + self.table_name + "` SET `current_branch_name` = ?, `current_element_name` = ? WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(branch_name), str(element_name), str(user_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def remove(self, user_id):
        """
        Удалить пользователя из базы данных
        > user_id идентификатор пользователя
        """
        sql_statement = "DELETE FROM `" + self.table_name + "` WHERE `user_id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def get(self, user_id):
        """
        Получить имя ветки и имя элемента
        > user_id идентификатор пользователя
        """
        sql_statement = "SELECT `current_branch_name`, `current_element_name` FROM `" + self.table_name + "` WHERE `user_id` = ?"

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
                r = {'current_branch_name': result[0], 'current_element_name': result[1]}
                return r

    def all(self):
        """
        Получить идентификаторы всех пользователей
        """
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

    def disconnect(self):
        """
        Разорвать связь с базой данных
        """
        self.connection.close()