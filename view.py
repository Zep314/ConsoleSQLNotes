# Вьювер - отображение данных и взаимодействие с пользователем

import time


class View:
    def __init__(self):
        pass

    @staticmethod
    def info():  # Информация
        print('Программа для ведения заметок с использованием MySQL сервера')
        print('Выполнена в качестве проекта промежуточной аттестации')
        print('на образовательном портале GeekBrains')
        print('Морданов Д.А. 2023г.')

    @staticmethod
    def buy():  # Вывод конечного сообщения
        print('Работа программы завершена.')

    @staticmethod
    def help():  # Вывод помощи
        print('Обрабатываются следующие команды:')
        print('\t /help - вывод помощи')
        print('\t /info - вывод информации о программе')
        print('\t /exit или /quit - выход из программы')
        print('\t /add  - добавить новую заметку')
        print('\t /edit - редактировать заметку')
        print('\t /del  - удалить заметку')
        print('\t /list - вывод списка заметок')
        print('\t /export - принудительно сохранить базу в файл JSON')
        print('\t /import - принудительно загрузить базу из файла JSON')

    @staticmethod
    def print(text):  # Просто печать (вдруг в будущем печать будет не на экран, а как то иначе)
        print(text)

    @staticmethod
    def select_record():  # Диалог запроса индекса записи
        return input('Введите номер записи для удаления, или -1 - для отмены действия: ')

    @staticmethod
    def add_edit():  # Диалог ввода данных для добавления или редактирования
        title: str = input('Введите заголовок заметки: ')
        note: str = input('Описание заметки: ')
        return title, note

    @staticmethod
    def show_records(data):  # Отображение базы данных на экране красиво
        def print_head():  # Печатаем заголовок таблицы
            print(
                f'{"-" * 1}Номер{"-" * 1}+{"-" * 11}Заголовок{"-" * 10}+'
                f'{"-" * 26}Заметка{"-" * 26}+{"-" * 7}Время{"-" * 7}')

        def print_footer():  # Печатаем низ таблицы
            print(f'{"-" * 7}+{"-" * 30}+{"-" * 59}+{"-" * 19}')

        def print_row(row):  # Печатаем одну строку таблицы с данными
            print(f'{list_data[row]["id"]:7}|{list_data[row]["title"]:30}|'
                  f'{list_data[row]["note"]:59}|{list_data[row]["datetime"]:11}')

        list_data = data.get_data()  # Тут должен быть список из словарей
        print('Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),')
        inp = input('или нажмите <Enter> для вывода всего списка: ')  # Запрос данных для фильтра по дате

        if len(inp) > 0:  # Фильтр задан
            try:
                valid_date = time.strptime(inp, '%d.%m.%Y')  # Проверяем фильтр - (должна быть корректная дата)
                print_head()
                for i in range(data.get_length()):
                    if time.strftime('%d.%m.%Y', valid_date) == list_data[i]['datetime'][:10]:  # Фильтрация данных
                        print_row(i)
                print_footer()
            except ValueError:
                print('Дата введена неверно!')
        else:  # Печатаем всю базу, без фильтрации
            print_head()
            for i in range(data.get_length()):
                print_row(i)
            print_footer()
