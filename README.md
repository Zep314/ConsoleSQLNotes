# Базы данных и SQL (семинары)
## Урок 2. SQL – создание объектов, простые запросы выборки

### **Задание:**

Дополнительное задание к первым 2 урокам: 
1. CRUD - операции на любом ЯП. Коннект с БД через С#, к примеру

#### Задача:

На предварительной аттестации у нас была следующая задача:

Реализовать консольное приложение заметки, с сохранением, чтением,
добавлением, редактированием и удалением заметок. Заметка должна
содержать идентификатор, заголовок, тело заметки и дату/время создания
или последнего изменения заметки. Сохранение заметок необходимо сделать
в формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой). Реализацию пользовательского интерфейса студент может
делать как ему удобнее, можно делать как параметры запуска программы
(команда, данные), можно делать как запрос команды с консоли и
последующим вводом данных, как-то ещё, на усмотрение студента.
При чтении списка заметок реализовать фильтрацию по дате.

Дополним ее взаимодействием с MySQL-сервером для оуществления всех операций с базой данных: 
создание, выборка, редактирование и удаление информации 
#### Критерии оценки:

Приложение должно запускаться без ошибок, должно уметь сохранять данные
в файл, уметь читать данные из файла, делать выборку по дате, выводить на
экран выбранную запись, выводить на экран весь список записок, добавлять
записку, редактировать ее и удалять.
***
### **Решение:**
Решение задачи без SQL (предыдущий вариант) представлено **[тут](https://github.com/Zep314/ConsoleNotes/)**
1. Собственно представлено дальнейшее развитие проекта с использованием MySQL сервера. 
2. Реализация проекта представлена в соответствующих файлах. Точка входа находится в файле _main.py_.
3. Результат работы программы представлен ниже.
***
### Результат работы программы:
    C:\Work\python\ConsoleSQLNotes>python ./main.py
    Программа для ведения заметок с использованием MySQL сервера
    Выполнена в качестве проекта промежуточной аттестации
    на образовательном портале GeekBrains
    Морданов Д.А. 2023г.
    Попытка соединиться с сервером localhost
    На сервере нет базы данных
    Создать базу данных? (yes/no): yes
    База данных создана!
    >>> /import
    Данные загружены из файла!
    >>> /list
    Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),
    или нажмите <Enter> для вывода всего списка:
    -Номер-+-----------Заголовок----------+--------------------------Заметка--------------------------+-------Время-------
          1|Beatles                       |Beatles образовались в 1960г.                              |02.02.2023 08:35:40
          2|Библиотека                    |ул. Весенняя, 60                                           |07.02.2023 08:36:31
          3|Лекарство для кота            |Полисорб, Смекта                                           |10.02.2023 08:37:47
          4|ТО для атомобиля              |Записаться 15.05.2023                                      |15.02.2023 08:38:37
    -------+------------------------------+-----------------------------------------------------------+-------------------
    >>> /add
    Добавление записи
    Введите заголовок заметки: Параметры доступа в БД
    Описание заметки: Сервер: 8.8.8.8; Логин: admin; Пароль: SuperPa$$w0rd
    Данные добавлены
    >>> /list
    Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),
    или нажмите <Enter> для вывода всего списка:
    -Номер-+-----------Заголовок----------+--------------------------Заметка--------------------------+-------Время-------
          1|Beatles                       |Beatles образовались в 1960г.                              |02.02.2023 08:35:40
          2|Библиотека                    |ул. Весенняя, 60                                           |07.02.2023 08:36:31
          3|Лекарство для кота            |Полисорб, Смекта                                           |10.02.2023 08:37:47
          4|ТО для атомобиля              |Записаться 15.05.2023                                      |15.02.2023 08:38:37
          5|Параметры доступа в БД        |Сервер: 8.8.8.8; Логин: admin; Пароль: SuperPa$$w0rd       |15.02.2023 10:12:05
    -------+------------------------------+-----------------------------------------------------------+-------------------
    >>> /list
    Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),
    или нажмите <Enter> для вывода всего списка: 10.02.2023
    -Номер-+-----------Заголовок----------+--------------------------Заметка--------------------------+-------Время-------
          3|Лекарство для кота            |Полисорб, Смекта                                           |10.02.2023 08:37:47
    -------+------------------------------+-----------------------------------------------------------+-------------------
    >>> /edit
    Введите номер записи для удаления, или -1 - для отмены действия: 2
    Редактирование записи
    Если данные менять не нужно - оставьте их пустыми
    Введите заголовок заметки:
    Описание заметки: переехала - ул. Летняя, 8/4
    Запись 2 успешно изменена! title => , note => переехала - ул. Летняя, 8/4
    >>> /list
    Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),
    или нажмите <Enter> для вывода всего списка:
    -Номер-+-----------Заголовок----------+--------------------------Заметка--------------------------+-------Время-------
          1|Beatles                       |Beatles образовались в 1960г.                              |02.02.2023 08:35:40
          2|Библиотека                    |переехала - ул. Летняя, 8/4                                |15.02.2023 10:13:08
          3|Лекарство для кота            |Полисорб, Смекта                                           |10.02.2023 08:37:47
          4|ТО для атомобиля              |Записаться 15.05.2023                                      |15.02.2023 08:38:37
          5|Параметры доступа в БД        |Сервер: 8.8.8.8; Логин: admin; Пароль: SuperPa$$w0rd       |15.02.2023 10:12:05
    -------+------------------------------+-----------------------------------------------------------+-------------------
    >>> /del
    Введите номер записи для удаления, или -1 - для отмены действия: 3
    Запись 3 удалена!
    >>> /list
    Введите дату за которую нужно вывести список заметок в формате (дд.мм.гггг),
    или нажмите <Enter> для вывода всего списка:
    -Номер-+-----------Заголовок----------+--------------------------Заметка--------------------------+-------Время-------
          1|Beatles                       |Beatles образовались в 1960г.                              |02.02.2023 08:35:40
          2|Библиотека                    |переехала - ул. Летняя, 8/4                                |15.02.2023 10:13:08
          4|ТО для атомобиля              |Записаться 15.05.2023                                      |15.02.2023 08:38:37
          5|Параметры доступа в БД        |Сервер: 8.8.8.8; Логин: admin; Пароль: SuperPa$$w0rd       |15.02.2023 10:12:05
    -------+------------------------------+-----------------------------------------------------------+-------------------
    >>> /quit
    Работа программы завершена.
