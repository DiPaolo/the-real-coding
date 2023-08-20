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

import hashlib
import os
import time


def bytes_to_human(byte_count):
    if byte_count < 1024:
        return f'{byte_count} bytes'
    elif byte_count < 1024 * 1024:
        return f'{byte_count / 1024 :.1f} KB'
    elif byte_count < 1024 * 1024 * 1024:
        return f'{byte_count / (1024 * 1024) :.1f} MB'
    elif byte_count < 1024 * 1024 * 1024 * 1024:
        return f'{byte_count / (1024 * 1024 * 1024) :.1f} GB'
    else:
        return f'{byte_count / (1024 * 1024 * 1024 * 1024) :.1f} TB'


def get_file_checksum_md5(filename: str) -> str:
    checksum = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buf = f.read(1024)
            if not buf:
                break
            checksum.update(buf)

    return checksum.hexdigest()


def print_dir_info(dir_name):
    total_files = 0
    total_bytes = 0
    total_time = 0

    for file in os.listdir(dir_name):
        full_filename = os.path.join(dir_name, file)
        if not os.path.isfile(full_filename):
            continue

        file_size = os.stat(full_filename).st_size

        start_time = time.perf_counter()
        md5 = get_file_checksum_md5(full_filename)
        end_time = time.perf_counter()

        total_files += 1
        total_bytes += file_size
        total_time += end_time - start_time

        print(f'{file}, {file_size} bytes ({bytes_to_human(file_size)}) MD5: {md5}')

    print(f'\n'
          f'Total: {total_files} files, {total_bytes} bytes ({bytes_to_human(total_bytes)})\n'
          f'Total time: {total_time:.02f} sec')


if __name__ == '__main__':
    print_dir_info('/Users/dipaolo/Downloads')
