# Контроллер - содержит главный цикл программы
# и объединяет представление и модель данных

from view import View
from model import Data
from log import add2log


class Controller:
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
            if self._data.edit(idx, title, note) != -1:  # Проверка на существование записи с таким номером
                self._view.print(f'Запись {idx} успешно изменена! title => {title}, note => {note}')
                add2log(f'Запись {idx} изменена! title => {title}, note => {note}', '>')
            else:
                self._view.print('Ошибка! Записи с таким индексом для редактирования не найдено!')
                add2log(f'Ошибка редактирования записи {str(idx)}. Записи не существует!', '>')

    def delete(self):  # Удаление данных из базы данных
        idx = int(self._view.select_record())  # Получение номера удаляемой записи
        if idx > -1:
            if self._data.delete(idx) != -1:  # Проверка на существование записи с таким номером
                self._view.print(f'Запись {idx} удалена!')
                add2log(f'Запись {idx} удалена!', '<')
            else:
                self._view.print('Ошибка! Записи с таким индексом для удаления не найдено!')
                add2log(f'Ошибка удаления записи {str(idx)}. Записи не существует!', '>')

    def list(self):  # Вывод данных на печать
        self._view.show_records(self._data)
        add2log(f'Выведено {self._data.get_length()} строк базы данных', '>')

    def load(self):  # Загрузка данных их файла
        self._data.load_db()
        self._view.print('Данные загружены из файла!')
        add2log('Данные загружены из файла.', '>')

    def save(self):  # Сохранение данных в файл
        self._data.save_db()
        self._view.print('Данные записаны в файл!')
        add2log('Данные записаны в файл.', '>')

    def run(self):
        self._view.info()  # Инфо программы
        #self.load()  # Загружаем базу данных
        while True:  # Главный цикл программы
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
#        self.save()  # Записываем данные на диск
        add2log('Завершение работы.', '>')
        self._view.buy()  # Прощаемся
