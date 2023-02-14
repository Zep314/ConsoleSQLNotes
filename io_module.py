# Модуль для работы с файлами

import os
import json


def export_json(data, file):  # Сохранение данных в файл в формате JSON
    if len(data) > 0:
        with open(file, 'w', encoding='UTF-8') as f:
            json.dump(data, f)


def import_json(file):  # Чтение файла в формате JSON и возврат их
    if os.path.isfile(file):
        with open(file, 'r', encoding='UTF-8') as f:
            return json.load(f)
    else:
        return []
