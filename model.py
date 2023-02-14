# Модель данных - содержит класс для хранения и организации данных,
# а так же методы для их обработки

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
# https://www.w3schools.com/python/python_mysql_create_db.asp

import time
import io_module
import settings
import mysql.connector
from mysql.connector import errorcode

class Data:

    def __init__(self):
        _connector = None

    # def add(self, title, note):  # Добавление данных по полям
    #     self._data.append({'id': self.get_max_id() + 1,
    #                        'title': title,
    #                        'note': note,
    #                        'datetime': time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(time.time()))
    #                        # Дату устанавливаем текущую
    #                        })
    #
    # def edit(self, idx, title, note):  # Редактирование данных
    #     pointer = -1
    #     for i in range(self.get_length()):  # Ищем запись по ее индексу
    #         if idx == int(self._data[i]['id']):
    #             pointer = i
    #             break
    #     if pointer == -1:  # Не нашли
    #         return -1
    #     else:  # Нашли, изменяем
    #         if len(title) > 0:
    #             self._data[pointer]['title'] = title
    #         if len(note) > 0:
    #             self._data[pointer]['note'] = note
    #         self._data[pointer]['datetime'] = time.strftime('%d.%m.%Y %H:%M:%S', time.gmtime(time.time()))
    #         # Дату устанавливаем текущую
    #         return 0
    #
    # def delete(self, idx):  # Удаление одной записи
    #     pointer = -1
    #     for i in range(self.get_length()):  # Ищем запись по ее индексу
    #         if idx == int(self._data[i]['id']):
    #             pointer = i
    #             break
    #     if pointer == -1:  # Не нашли такую запись
    #         return -1
    #     else:
    #         del self._data[pointer]  # Нашли, удаляем
    #         return 0
    #
    # def save_db(self):  # Сохраняем данные
    #     if self._data is not None:
    #         io_module.save_json(self._data, settings.db_file)
    #
    # def load_db(self):  # Загружаем данные
    #     self._data.clear()  # Почистим старые данные
    #     self._data = io_module.load_json(settings.db_file)
    #
    # def get_length(self):  # Возвращаем количество записей
    #     return len(self._data) if self._data is not None else 0
    #
    # def get_max_id(self):  # Ищем максимальный ID у записей
    #     return max([i['id'] for i in self._data]) if self.get_length() > 0 else 0
    #
    # def get_data(self):  # Выдаем всю базу (для записи в файл)
    #     return self._data[:] if self._data is not None else []

    def connect(self):
        try:
            self._connector = mysql.connector.connect(
                                user = settings.db_login,
                                password = settings.db_passwd,
                                host = settings.db_server)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
