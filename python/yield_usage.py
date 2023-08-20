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


def get_file_checksum_md5(filename: str):
    checksum = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buf = f.read(1024)
            if not buf:
                break
            checksum.update(buf)
            yield None

    yield checksum.hexdigest()


def print_dir_info(dir_name):
    total_files = 0
    total_bytes = 0
    for file in os.listdir(dir_name):
        full_filename = os.path.join(dir_name, file)
        if not os.path.isfile(full_filename):
            continue

        file_size = os.stat(full_filename).st_size
        gen = get_file_checksum_md5(full_filename)
        while True:
            print(next(gen))

        total_files += 1
        total_bytes += file_size

        print(f'{file}, {file_size} bytes ({bytes_to_human(file_size)}) MD5: {md5}')

    print(f'\n'
          f'Total: {total_files} files, {total_bytes} bytes ({bytes_to_human(total_bytes)})')


if __name__ == '__main__':
    gen = get_file_checksum_md5('/Users/dipaolo/Downloads/org.gimp.GIMP.flatpakref')
    # while True:
    while True:
        ret = next(gen)
        print(f'{ret}')
        if ret is not None:
            break

    for iii in get_file_checksum_md5('/Users/dipaolo/Downloads/org.gimp.GIMP.flatpakref'):
        print(iii)

    # print_dir_info('/Users/dipaolo/Downloads')

# X = 0
#
#
# def process():
#     global X
#     x = 0
#     for _ in range(0, 10):
#         x += 1
#         X += 1
#         print(f'   {x}   {X}')
#         yield x
#
#
# for i in range(0, 7):
#     print(next(process()))
#
#
# def infinite_sequence():
#     num = 0
#     while True:
#         yield num
#         num += 1
#
#
# sss = infinite_sequence()
# print(next(sss))
# print(next(sss))
# print(next(sss))

# print(next(process()))
# print(next(process()))
#
# rrr = next(process())
# print(f'{rrr} type of "{type(rrr)}"')
# process()
#
# print(X)
#
# next(i for i in process())
# next(i for i in process())
# next(i for i in process())
# next(i for i in process())
