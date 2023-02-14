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
        self._connector = None

    def __del__(self):
        self._connector.close()

    def add(self, title, note):  # Добавление данных по полям
        sql = f'INSERT INTO notes (title,note) VALUES (\'{title}\',\'{note}\');'
        mycursor = self._connector.cursor()
        mycursor.execute(sql)
        self._connector.commit()
        mycursor.close()

    def edit(self, idx, title, note):  # Редактирование данных
        sql = f'UPDATE notes SET title=\'{title}\', note=\'{note}\', dt=now() WHERE id = {idx};';
        mycursor = self._connector.cursor()
        mycursor.execute(sql)
        self._connector.commit()
        ret = mycursor.rowcount
        mycursor.close()
        return ret

    def delete(self, idx):  # Удаление одной записи
        sql = f'DELETE FROM notes WHERE id = {idx};'
        mycursor = self._connector.cursor()
        mycursor.execute(sql)
        self._connector.commit()
        ret = mycursor.rowcount
        mycursor.close()
        return ret

    def export_db(self):  # Сохраняем данные
        io_module.export_json(self.get_data(), settings.external_file)

    def import_db(self):  # Загружаем данные
        sql = f'DELETE FROM notes;'
        mycursor = self._connector.cursor()
        mycursor.execute(sql)
        data = io_module.import_json(settings.external_file)
        for row in data:
            sql = f'INSERT INTO notes (title,note,dt) VALUES (\'{row["title"]}\',\'{row["note"]}\',\'{time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(row["datetime"],"%d.%m.%Y %H:%M:%S"))}\');'
            mycursor.execute(sql)
        self._connector.commit()
        mycursor.close()

    def get_data(self, dt = ''):  # Выдаем всю базу (для записи в файл)
        sql = f'SELECT id, title, note, DATE_FORMAT(dt,\'%d.%m.%Y %H:%i:%S\') FROM notes'
        if len(dt) > 0:
            sql += f' WHERE CAST(dt as DATE) = \'{dt}\''
        sql += ';'
        mycursor = self._connector.cursor()
        mycursor.execute(sql)
        ret = [{'id': id, 'title': title, 'note': note, 'datetime': dt} for (id, title, note, dt) in mycursor]
        self._connector.commit()
        mycursor.close()
        return ret

    def connect(self):
        try:
            self._connector = mysql.connector.connect(
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
            return settings.DB_OK

    def create_db(self):
        self._connector = mysql.connector.connect(
            user=settings.db_login,
            password=settings.db_passwd,
            host=settings.db_server,
            auth_plugin='mysql_native_password'
        )
        mycursor = self._connector.cursor()
        sql = 'DROP DATABASE IF EXISTS notes;'
        mycursor.execute(sql)

        sql = 'CREATE DATABASE notes;'
        mycursor.execute(sql)
        sql = 'DROP TABLE IF EXISTS notes.notes;'
        mycursor.execute(sql)
        sql = 'CREATE TABLE notes.notes (' \
              '  id BIGINT auto_increment NOT NULL,' \
              '  title varchar(30) NULL,' \
              '  note varchar(100) NULL,' \
              '  dt DATETIME DEFAULT now() NULL,' \
              '  PRIMARY KEY (id)' \
              ')' \
              'ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'
        mycursor.execute(sql)
        mycursor.close()