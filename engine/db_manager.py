import sqlite3
from data.config import DB_CONFIG_TABLE_NAME, DB_USER_TABLE_NAME, DB_ELEMENT_TABLE_NAME, \
    DB_ELEMENT_ADDITION_TABLE_NAME, DB_ELEMENT_TRANSITION_TABLE_NAME, DB_SCHEME_TABLE_NAME, DB_PATH

class DbManager(object):
    """
    Работа с базой данных
    """

    def __init__(self):
        """
        Конструктор (подключение к базе данных)
        """
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, element_id, messenger_id):
        """
        """
        sql_statement = "INSERT INTO `" + DB_USER_TABLE_NAME + \
                        "` (`user_id`, `messenger_id`, `element_id`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_id), str(messenger_id), str(element_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_user(self, user_id, new_element_id, new_messenger_id):
        """
        """
        sql_statement = "UPDATE `" + DB_USER_TABLE_NAME + \
                        "` SET `element_id` = ?, `messenger_id` = ? WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_element_id), str(new_messenger_id), str(user_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_user_data(self, user_id):
        """
        """
        sql_statement = "SELECT `id`, `user_id`, `element_id`, `messenger_id` FROM `" + DB_USER_TABLE_NAME + \
                        "` WHERE `user_id` = ?"

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
                r = {'id': result[0], 'user_id': result[1], 'element_id': result[2], 'messenger_id': result[3]}
                return r

    def add_config(self, token, messenger_id, is_on):
        """
        """
        sql_statement = "INSERT INTO `" + DB_CONFIG_TABLE_NAME + \
                        "` (`messenger_id`, `token`, `is_on`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(messenger_id), str(token), str(is_on)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_config(self, token, new_messenger_id, new_token, new_is_on):
        """
        """
        sql_statement = "UPDATE `" + DB_CONFIG_TABLE_NAME + \
                        "` SET `messenger_id` = ?, `token` = ?, `is_on` = ? WHERE `token` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_messenger_id), str(new_token), str(new_is_on), str(token)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_config_data(self, token):
        """
        """
        sql_statement = "SELECT `id`, `messenger_id`, `token`, `is_on` FROM `" + DB_CONFIG_TABLE_NAME + \
                        "` WHERE `token` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(token),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0],'messenger_id': result[1], 'token': result[2], 'is_on': result[3]}
                return r

    def add_scheme(self, name):
        """
        """
        sql_statement = "INSERT INTO `" + DB_SCHEME_TABLE_NAME + \
                        "` (`name`) VALUES(?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(name)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_scheme(self, name, new_name):
        """
        """
        sql_statement = "UPDATE `" + DB_SCHEME_TABLE_NAME + \
                        "` SET `name` = ? WHERE `name` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_name), str(name)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_scheme_data(self, name):
        """
        """
        sql_statement = "SELECT `id` FROM `" + DB_SCHEME_TABLE_NAME + \
                        "` WHERE `name` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0], 'name': name}
                return r
    def remove_scheme(self, name):
        """
        """
        sql_statement = "DELETE FROM `" + DB_SCHEME_TABLE_NAME + "` WHERE `name` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def add_element(self, name, text, scheme_id):
        """
        """
        sql_statement = "INSERT INTO `" + DB_ELEMENT_TABLE_NAME + \
                        "` (`name`, `text`, `scheme_id`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(name), str(text), str(scheme_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_element(self, name, new_text):
        """
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_TABLE_NAME + \
                        "` SET `text` = ? WHERE `name` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_text), str(name)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_element_data(self, name):
        """
        """
        sql_statement = "SELECT `id`, `name`, `text`, `scheme_id` FROM `" + DB_ELEMENT_TABLE_NAME + \
                        "` WHERE `name` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0], 'name': result[1], 'text': result[2], 'scheme_id': result[3]}
                return r
    def remove_element(self, name):
        """
        """
        sql_statement = "DELETE FROM `" + DB_SCHEME_TABLE_NAME + "` WHERE `name` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_all_additions_id_from_element(self, name):
        """
        """
        element_id = self.get_element_data(name)['id']

        sql_statement = "SELECT `id` FROM `" + DB_ELEMENT_ADDITION_TABLE_NAME + \
                        "` WHERE `element_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(element_id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                return result
    def get_all_transitions_id_from_element(self, name):
        """
        """
        element_id = self.get_element_data(name)['id']

        sql_statement = "SELECT `id` FROM `" + DB_ELEMENT_TRANSITION_TABLE_NAME + \
                        "` WHERE `element_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(element_id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                return result

    def add_addition(self, element_id, addition_id, text):
        """
        """
        sql_statement = "INSERT INTO `" + DB_ELEMENT_ADDITION_TABLE_NAME + \
                        "` (`addition_id`, `text`, `element_id`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(addition_id), str(text), str(element_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_addition(self, id, new_addition_id, new_text):
        """
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_ADDITION_TABLE_NAME + \
                        "` SET `addition_id` = ?, `text` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_addition_id), str(new_text), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_addition_data(self, id):
        """
        """
        sql_statement = "SELECT `id`, `addition_id`, `text`, `element_id` FROM `" + DB_ELEMENT_ADDITION_TABLE_NAME + \
                        "` WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0], 'addition_id': result[1], 'text': result[2], 'element_id': result[3]}
                return r
    def remove_addition(self, id):
        """
        """
        sql_statement = "DELETE FROM `" + DB_ELEMENT_ADDITION_TABLE_NAME + "` WHERE `id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def add_transition(self, element_id, transition_id, text):
        """
        """
        sql_statement = "INSERT INTO `" + DB_ELEMENT_TRANSITION_TABLE_NAME + \
                        "` (`transition_id`, `text`, `element_id`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(transition_id), str(text), str(element_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def update_transition(self, id, new_transition_id, new_text):
        """
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_TRANSITION_TABLE_NAME + \
                        "` SET `transition_id` = ?, `text` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_transition_id), str(new_text), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_transition_data(self, id):
        """
        """
        sql_statement = "SELECT `id`, `transition_id`, `text`, `element_id` FROM `" + DB_ELEMENT_TRANSITION_TABLE_NAME + \
                        "` WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0], 'transition_id': result[1], 'text': result[2], 'element_id': result[3]}
                return r
    def remove_transition(self, id):
        """
        """
        sql_statement = "DELETE FROM `" + DB_ELEMENT_TRANSITION_TABLE_NAME + "` WHERE `id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    def disconnect(self):
        """
        Разорвать связь с базой данных
        """
        self.connection.close()


if __name__ == '__main__':
    dbm = DbManager()
    print(dbm.get_all_additions_id_from_element("тест"))