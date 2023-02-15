# Контроллер - содержит главный цикл программы
# и объединяет представление и модель данных

from view import View
from model import Data
from log import add2log
import settings


class Controller:
    _data: Data = None

    def __init__(self):
        self._view = View()  # объект представления
        self._data = Data()  # объект данных

    def add(self):  # Добавление данных в базу данных
        self._view.print('Добавление записи')
        title, note = self._view.add_edit()  # получение данных из вьювера
        self._data.add(title, note)
        self._view.print('Данные добавлены')
        add2log(f'Добавление данных: Title = {title}; Note = {note} ', '<')

    def edit(self):  # Редактирование данных
        idx = int(self._view.select_record())  # Получение номера редактируемой записи
        if idx > -1:
            self._view.print('Редактирование записи')
            self._view.print('Если данные менять не нужно - оставьте их пустыми')
            title, note = self._view.add_edit()  # Получаем данные для изменения
            if self._data.edit(idx, title, note) > 0:  # Проверка на существование записи с таким номером
                self._view.print(f'Запись {idx} успешно изменена! title => {title}, note => {note}')
                add2log(f'Запись {idx} изменена! title => {title}, note => {note}', '>')
            else:
                self._view.print('Ошибка! Записи с таким индексом для редактирования не найдено!')
                add2log(f'Ошибка редактирования записи {str(idx)}. Записи не существует!', '>')

    def delete(self):  # Удаление данных из базы данных
        idx = int(self._view.select_record())  # Получение номера удаляемой записи
        if idx > -1:
            if self._data.delete(idx) > 0:  # Проверка на существование записи с таким номером
                self._view.print(f'Запись {idx} удалена!')
                add2log(f'Запись {idx} удалена!', '<')
            else:
                self._view.print('Ошибка! Записи с таким индексом для удаления не найдено!')
                add2log(f'Ошибка удаления записи {str(idx)}. Записи не существует!', '>')

    def list(self):  # Вывод данных на печать
        result_rows = self._view.show_records(self._data)
        add2log(f'Выведено {result_rows} строк базы данных', '>')

    def load(self):  # Загрузка данных их файла
        self._data.import_db()
        self._view.print('Данные загружены из файла!')
        add2log('Данные загружены из файла.', '>')

    def save(self):  # Сохранение данных в файл
        self._data.export_db()
        self._view.print(f'Данные записаны в файл {settings.external_file}')
        add2log(f'Данные записаны в файл {settings.external_file}', '>')

    def main_loop(self):  # Главный цикл программы
        while True:
            inp = input('>>> ')
            add2log(inp, '>')  # Записываем в журнал все, что вводят
            match inp.lower():
                case '/exit':
                    break
                case '/quit':
                    break
                case '/help':
                    self._view.help()
                case '/add':
                    self.add()
                case '/edit':
                    self.edit()
                case '/del':
                    self.delete()
                case '/list':
                    self.list()
                case '/export':
                    self.save()
                case '/import':
                    self.load()
                case _:
                    self._view.print('Неверная команда. Для помощи наберите /help')
        del self._data

    def run(self):
        self._view.info()  # Инфо программы
        self._view.print(f'Попытка соединиться с сервером {settings.db_server}')
        add2log(f'Попытка соединиться с сервером {settings.db_server}', '>')
        match self._data.connect():
            case settings.DB_LOGIN_ERROR:
                self._view.print('Неверный логин/пароль для серверу')
                add2log('Неверный логин/пароль для серверу', '>')
            case settings.DB_NO_CONNECT:
                self._view.print('Нет соединения с сервером')
                add2log('Нет соединения с сервером', '>')
            case settings.DB_NO_DATABASE_EXIST:
                self._view.print('На сервере нет базы данных')
                add2log('На сервере нет базы данных', '>')
                user_input = input('Создать базу данных? (yes/no): ')
                if user_input.lower() in ['yes', 'y']:
                    self._data.create_db()
                    self._view.print('База данных создана!')
                    add2log('База данных создана!', '>')
                    self.main_loop()
            case settings.DB_OK:
                self._view.print(f'Cоединение с сервером {settings.db_server} установлено')
                add2log(f'Cоединение с сервером {settings.db_server} установлено', '>')
                self.main_loop()
            case _:
                self._view.print('Неизвестная ошибка')
                add2log('Неизвестная ошибка', '>')
        add2log('Завершение работы.', '>')
        self._view.buy()  # Прощаемся
