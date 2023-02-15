# Модель данных - содержит класс для заимодействия с сервером SQL и организации данных,
# а так же методы для их обработки

import time
import io_module
import settings
import mysql.connector
from mysql.connector import errorcode


class Data:

    def __init__(self):
        self._connector = None

    def __del__(self): # Деструктор - в нем закрываем соединение с SQL сервером, если оно было открыто
        if self._connector is not None:
            self._connector.close()

    def add(self, title, note):  # Добавление данных по полям
        sql = f'INSERT INTO notes (title,note) VALUES (\'{title}\',\'{note}\');'
        my_cursor = self._connector.cursor()
        my_cursor.execute(sql)
        self._connector.commit()
        my_cursor.close()

    def edit(self, idx, title, note):  # Редактирование данных
        sql = f'UPDATE notes SET '
        if len(title) == 0 and len(note) == 0:  # Логика, если какое-то поле не ввели - его не изменяем
            return 0
        elif len(title) > 0 and len(note) > 0:
            sql += f'title=\'{title}\', note=\'{note}\''
        elif len(title) > 0:
            sql += f'title=\'{title}\''
        else:
              sql += f'note=\'{note}\''
        sql += f', dt=now() WHERE id = {idx};'
        my_cursor = self._connector.cursor()
        my_cursor.execute(sql)
        self._connector.commit()
        ret = my_cursor.rowcount
        my_cursor.close()
        return ret

    def delete(self, idx):  # Удаление одной записи
        sql = f'DELETE FROM notes WHERE id = {idx};'
        my_cursor = self._connector.cursor()
        my_cursor.execute(sql)
        self._connector.commit()
        ret = my_cursor.rowcount
        my_cursor.close()
        return ret

    def export_db(self):  # Сохраняем данные
        io_module.export_json(self.get_data(''), settings.external_file)

    def import_db(self):  # Загружаем данные
        sql = f'DELETE FROM notes;'
        my_cursor = self._connector.cursor()
        my_cursor.execute(sql)    # Чистим старые данные
        data = io_module.import_json(settings.external_file)
        for row in data:          # Грузим новые данные
            sql = f'INSERT INTO notes (title,note,dt) VALUES (\'{row["title"]}\',\'{row["note"]}\'' \
                  f',\'{time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(row["datetime"], "%d.%m.%Y %H:%M:%S"))}\');'
            my_cursor.execute(sql)
        self._connector.commit()
        my_cursor.close()

    def get_data(self, dt):  # Выдаем всю базу (для записи в файл или печати)
        sql = f'SELECT id, title, note, DATE_FORMAT(dt,\'%d.%m.%Y %H:%i:%S\') FROM notes'
        if len(dt) > 0:  # докидываем фильтр по дате, если он есть
            sql += f' WHERE CAST(dt as DATE) = \'{dt}\''
        sql += ';'
        my_cursor = self._connector.cursor()
        my_cursor.execute(sql)
        # Генерируем данные
        ret = [{'id': id1, 'title': title, 'note': note, 'datetime': dt} for (id1, title, note, dt) in my_cursor]
        my_cursor.close()
        return ret

    def connect(self):  # Метод - попытка соединиться с SQL сервером, и выдача результата операции
        try:
            self._connector = mysql.connector.connect(  # Пытаемся соединиться с указанием имени базы данных
                user=settings.db_login,
                password=settings.db_passwd,
                host=settings.db_server,
                database=settings.db_base,
                auth_plugin='mysql_native_password'
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return settings.DB_LOGIN_ERROR
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                return settings.DB_NO_DATABASE_EXIST
            else:
                return settings.DB_NO_CONNECT
        else:
            return settings.DB_OK  # тут self._connector будет не none

    def create_db(self):  # Создаем базу данных и таблицу в ней
        self._connector = mysql.connector.connect(  # Заново соединяемся с сервером без указания имени базы данных
            user=settings.db_login,
            password=settings.db_passwd,
            host=settings.db_server,
            auth_plugin='mysql_native_password'
        )
        my_cursor = self._connector.cursor()
        sql = 'DROP DATABASE IF EXISTS notes;'
        my_cursor.execute(sql)

        sql = 'CREATE DATABASE notes;'
        my_cursor.execute(sql)

        sql = 'USE notes;'
        my_cursor.execute(sql)

        sql = 'DROP TABLE IF EXISTS notes.notes;'
        my_cursor.execute(sql)
        sql = 'CREATE TABLE notes.notes (' \
              '  id BIGINT auto_increment NOT NULL,' \
              '  title varchar(30) NULL,' \
              '  note varchar(100) NULL,' \
              '  dt DATETIME DEFAULT now() NULL,' \
              '  PRIMARY KEY (id)' \
              ')' \
              'ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'
        my_cursor.execute(sql)
        my_cursor.close()
