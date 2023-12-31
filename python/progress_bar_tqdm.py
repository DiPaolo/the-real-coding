#!/usr/bin/python3
#
#
# == описание ==
# скрипт, который демонстрирует работу прогресс бара в командной строке,
# используя пакет tqdm
#
#
# == алгоритм работы ==
#   1. генерируем список файлов
#   2. создаем и настраиваем прогресс бар
#   3. производим эмуляцию обработки файла (засыпаем на время)
#   4. обновляем прогресс бар для визуализации процесса
#
#
# == указания ==
#
# нужно поставить пакет tqdm:
#   > pip install tqdm
# либо поставить его через IDE
#

import random
import string
import time

from tqdm import tqdm


def generate_random_filename(length: int) -> str:
    # обрати внимание!
    # добавляем 15 символов подчеркивания ('_'), чтобы повысить вероятность
    # добавления этого символа в имя файла; такой символ обычно используют
    # вместо пробелов в именах файлов
    return ''.join(random.choice(string.ascii_letters + string.digits + 15 * '_') for _ in range(0, length))


def generate_filenames(n):
    # генерируем n имен файлов;
    # каждое имя файла случайной длины от 6 до 16 символов
    return [f'{generate_random_filename(random.randint(6, 16))}.txt' for _ in range(0, n)]


def process_file(filename):
    # имитация обработки;
    # для этого просто засыпаем на рандомное время от 1 до 200 миллисекунд
    # в реальном проекте тут может быть:
    #   - поиск слова в файле
    #   - транскодирование файла
    #   - подсчет MD5 чек-суммы
    #   - поиск лиц на изображении и т.д.
    time.sleep(random.randint(1, 200) / 1000.0)


if __name__ == '__main__':
    # генерируем список файлов;
    # при этом выбираем случайное количество файлов для
    # большего интереса ;)
    files = generate_filenames(random.randint(20, 100))

    # создаем объект прогресс бара, даем ему отображаемое название +
    # указываем, сколько элементов мы планируем обработать
    progress_bar = tqdm(files, desc='Processing files', total=len(files))
    for file in files:
        # обрабатываем файл
        process_file(file)

        # обновляем прогресс бар (по умолчанию на 1 элемент);
        # прогресс бар при это обновит проценты и свои визуальные деления
        progress_bar.update()
