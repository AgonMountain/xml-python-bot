import sqlite3
from data.config import DB_CONFIG_TABLE_NAME, DB_USER_TABLE_NAME, DB_ELEMENT_TABLE_NAME, \
    DB_ELEMENT_ADDITION_TABLE_NAME, DB_ELEMENT_TRANSITION_TABLE_NAME, DB_SCHEME_TABLE_NAME, DB_MESSENGER_TABLE_NAME, \
    DB_NEED_FOR_UPDATE_XML

class DbManager(object):
    """
    Работа с базой данных
    """

    def __init__(self, DB_PATH):
        """
        Конструктор (подключение к базе данных)
        """
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
    def disconnect(self):
        """
        Разорвать связь с базой данных
        """
        self.connection.close()
    def return_id(self, table, key, value):
        """

        """
        sql_statement = "SELECT `id` FROM `" + table + \
                        "` WHERE `" + key +  "` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(value),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return result[0]

    def get_config(self, messenger_name):
        """
        """
        messenger_id = self.get_messenger_id(messenger_name)

        sql_statement = "SELECT `id`, `messenger_id`, `token`, `is_on` FROM `" + DB_CONFIG_TABLE_NAME + \
                        "` WHERE `messenger_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(messenger_id),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                r = {'id': result[0], 'messenger_id': result[1], 'token': result[2], 'is_on': result[3]}
                return r

    def get_need_for_update_xml(self):
        """
        """
        sql_statement = "SELECT `need_update` FROM `" + DB_NEED_FOR_UPDATE_XML + \
                        "` WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(1),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            if result == None:
                return result
            else:
                return result[0]
    def update_need_for_update_xml(self, need_update):
        """
        """
        sql_statement = "UPDATE `" + DB_NEED_FOR_UPDATE_XML + \
                        "` SET `need_update` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(need_update), str(1)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    # TODO
    def from_list_to_glossary(self, list):
        pass


    """ Работа с пользователями """
    def add_user(self, user_messenger_id, element_id, messenger_id):
        """
        Добавить пользователя
        @param user_messenger_id id пользователя внутри мессенджера
        @param element_id id элемента на котором остановился пользователь
        @param messenger_id id мессенджера
        """
        sql_statement = "INSERT INTO `" + DB_USER_TABLE_NAME + \
                        "` (`user_id`, `messenger_id`, `element_id`) VALUES(?,?,?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(user_messenger_id), str(messenger_id), str(element_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return self.return_id(DB_USER_TABLE_NAME, 'user_id', user_messenger_id)
    def update_user(self, user_messenger_id, new_element_id):
        """
        Обновить данные пользователя
        @param user_messenger_id id пользователя внутри мессенджера
        @param new_element_id id элемента
        """
        sql_statement = "UPDATE `" + DB_USER_TABLE_NAME + \
                        "` SET `element_id` = ? WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_element_id), str(user_messenger_id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_user_data(self, user_messenger_id):
        """
        Получить данные пользователя
        @param user_messenger_id id пользователя внутри мессенджера
        @return {'id', 'user_id', 'element_id', 'messenger_id'}
        """
        sql_statement = "SELECT `id`, `user_id`, `element_id`, `messenger_id` FROM `" + DB_USER_TABLE_NAME + \
                        "` WHERE `user_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(user_messenger_id),))
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
    def clean_table_user(self):
        """
        Очистить таблицу с пользователями
        """
        sql_statement = "DELETE FROM `" + DB_USER_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    """ Работа с мессенджарами """
    def get_messenger_id(self, name):
        """
        Получить все мессенджеры ("типы")
        @param name имя мессенджера
        @return id
        """
        sql_statement = "SELECT `id` FROM `" + DB_MESSENGER_TABLE_NAME + "` WHERE `name` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchone()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return result[0]

    """ Работа с конфигурациями """
    def add_config(self, token, messenger_id, is_on):
        """
        Добавить конфигурацию
        @param token токен для подключения бота к мессенджеру
        @param messenger_id id мессенджера
        @param is_on состояние активности бота
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
            return self.return_id(DB_CONFIG_TABLE_NAME, 'token', token)
    def update_config(self, id, new_token, new_is_on):
        """
        Обновить данные конфигурации
        @param id id конфигурации
        @param new_token новый токен для подключения бота к мессенджеру
        @param new_is_on новое состояние активности бота
        """
        sql_statement = "UPDATE `" + DB_CONFIG_TABLE_NAME + \
                        "` SET `token` = ?, `is_on` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_token), str(new_is_on), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_all_configs(self):
        """
        Получить все конфигурации в виде списка списков, содержащих данные конфигурации
        @return [ ('id', 'messenger_id', 'token', 'is_on') ]
        """
        sql_statement = "SELECT `id`, `messenger_id`, `token`, `is_on` FROM `" + DB_CONFIG_TABLE_NAME + "`"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return result
    def get_config_data(self, id):
        """
        Получить данные конфигурации
        @param token токен для подключения бота к мессенджеру, по которму мы будет искать конфигурацию для получения данных
        @return {'id', 'messenger_id', 'token', 'is_on'}
        """
        sql_statement = "SELECT `id`, `messenger_id`, `token`, `is_on` FROM `" + DB_CONFIG_TABLE_NAME + \
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
                r = {'id': result[0], 'messenger_id': result[1], 'token': result[2], 'is_on': result[3]}
                return r
    def clean_table_config(self):
        """
        Очистить таблицу с конфигурациями
        """
        sql_statement = "DELETE FROM `" + DB_CONFIG_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    """ Работа с схемами """
    def add_scheme(self, name):
        """
        Добавить схему
        @param name имя схемы
        """
        sql_statement = "INSERT INTO `" + DB_SCHEME_TABLE_NAME + \
                        "` (`name`) VALUES(?)"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(name),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return self.return_id(DB_SCHEME_TABLE_NAME, 'name', name)
    def update_scheme(self, id, new_name):
        """
        Обновить данные схемы
        @param id имя схемы, по которому мы будет искать схему для обновления
        @param new_name новое имя схемы
        """
        sql_statement = "UPDATE `" + DB_SCHEME_TABLE_NAME + \
                        "` SET `name` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_name), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_all_schemes(self):
        """
        Получить все схемы в виде списка списков, содержащих данные схемы
        @return [ ('id', 'name') ]
        """
        sql_statement = "SELECT `id`, `name` FROM `" + DB_SCHEME_TABLE_NAME + "`"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return result
    def get_scheme_data(self, id):
        """
        Получить данные схемы
        @param id id схемы
        @return {'id', 'name'}
        """
        sql_statement = "SELECT `name` FROM `" + DB_SCHEME_TABLE_NAME + \
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
                r = {'id': id, 'name': result[0]}
                return r
    def remove_scheme(self, id):
        """
        Удалить схему
        @param id имя схемы
        """
        sql_statement = "DELETE FROM `" + DB_SCHEME_TABLE_NAME + "` WHERE `id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def clean_table_scheme(self):
        """
        Очистить таблицу с схеами
        """
        sql_statement = "DELETE FROM `" + DB_SCHEME_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    """ Работа с элементами """
    def add_element(self, name, text, scheme_id):
        """
        Добавить элемент
        @param name имя элемента
        @param text текст элемента
        @param scheme_id id схемы
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
            return self.return_id(DB_ELEMENT_TABLE_NAME, 'name', name)
    def update_element(self, id, new_name, new_text):
        """
        Обновить данные элемента
        @param id id элемента
        @param new_name новое имя элемента
        @param new_text новый текст элемента
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_TABLE_NAME + \
                        "` SET `name` = ?, `text` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_name), str(new_text), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_all_elements(self, scheme_id):
        """
        Получить все элемент схемы в виде списка списков, содержащих данные элемента
        @param scheme_id id схемы
        @return [ ('id', 'name', 'text', 'scheme_id') ]
        """
        sql_statement = "SELECT `id`, `name`, `text`, `scheme_id` FROM `" + DB_ELEMENT_TABLE_NAME + \
                        "` WHERE `scheme_id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(scheme_id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
            return result
    def get_element_id(self, name):
        """
        Получить id элемента
        @param name имя элемента
        @return id
        """
        sql_statement = "SELECT `id` FROM `" + DB_ELEMENT_TABLE_NAME + \
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
                return result[0]
    def get_element_data(self, id):
        """
        Получить данные элемента
        @param id id элемента
        @return [ {'id', 'name', 'text', 'scheme_id'} ]
        """
        sql_statement = "SELECT `id`, `name`, `text`, `scheme_id` FROM `" + DB_ELEMENT_TABLE_NAME + \
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
                r = {'id': result[0], 'name': result[1], 'text': result[2], 'scheme_id': result[3]}
                return r
    def get_all_additions_id_from_element(self, element_id):
        """
        Получить все id дополнений элемента в виде списка
        @param element_id id элемента
        @return [ id, ]
        """
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
    def get_all_transitions_id_from_element(self, element_id):
        """
        Получить все id переходов элемента в виде списка
        @param element_id id элемента
        @return [ id, ]
        """
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
    def remove_element(self, id):
        """
        Удалить элемент
        @param id id элемента
        """
        sql_statement = "DELETE FROM `" + DB_SCHEME_TABLE_NAME + "` WHERE `id` = ?"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement, (str(id),))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def clean_table_element(self):
        """
        Очистить таблицу с элементами
        """
        sql_statement = "DELETE FROM `" + DB_ELEMENT_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    """ Работа с дополнениями """
    def add_addition(self, element_id, addition_id, text):
        """
        Добавить дополнение
        @param element_id id элемента, которому принадлежит дополнение
        @param addition_id id элемента, которое будет служить дополнением
        @param text текст / условие вывода дополнения
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
    def update_addition(self, id, new_text):
        """
        Обновить данные дополнения
        @param id id дополнения
        @param new_text новый текст / условие вывода дополнения
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_ADDITION_TABLE_NAME + \
                        "` SET `text` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_text), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_addition_data(self, id):
        """
        Получить данные дополнения
        @param id id дополнения
        @return {'id', 'addition_id', 'text', 'element_id'}
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
        Удалить дополнение
        @param id id дополнения
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
    def clean_table_addition(self):
        """
        Очистить таблицу с дополнениями
        """
        sql_statement = "DELETE FROM `" + DB_ELEMENT_ADDITION_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()

    """ Работа с переходами """
    def add_transition(self, element_id, transition_id, text):
        """
        Добавить переход
        @param element_id id элемента, которому принадлежит переход
        @param transition_id id элемента, на который будет выполнен переход
        @param text текст / условие перехода
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
    def update_transition(self, id, new_text):
        """
        Обновить данные перехода
        @param id id перехода
        @param new_text новый текст / условие перехода
        """
        sql_statement = "UPDATE `" + DB_ELEMENT_TRANSITION_TABLE_NAME + \
                        "` SET `text` = ? WHERE `id` = ?"

        '''Выполнение запроса + обработка ошибки'''
        try:
            self.cursor.execute(sql_statement, (str(new_text), str(id)))
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
    def get_transition_data(self, id):
        """
        Получить данные перехода
        @param id id перехода
        @return {'id', 'transition_id', 'text', 'element_id'}
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
        Удалить переход
        @param id id перехода
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
    def clean_table_transition(self):
        """
        Очистить таблицу с переходами
        """
        sql_statement = "DELETE FROM `" + DB_ELEMENT_TRANSITION_TABLE_NAME + "`"

        """Выполнение запроса + обработка ошибки"""
        try:
            self.cursor.execute(sql_statement)
            result = self.cursor.fetchall()
        except sqlite3.DatabaseError as error:
            print('Error:', error)
        else:
            self.connection.commit()
