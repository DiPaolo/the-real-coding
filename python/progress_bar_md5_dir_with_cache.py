#!/usr/bin/python3
#
#
# == описание ==
# скрипт, который
#
#
# == алгоритм работы ==
#   1.
#   2.
#   3.
#   4.
#
#
# == указания ==
#
# нужно поставить пакет :
#   > pip install
# либо поставить его через IDE
#
import hashlib
import os
import random
import time
from functools import lru_cache


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


@lru_cache(maxsize=256)
def get_file_checksum_md5_cached(filename: str) -> str:
    checksum = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buf = f.read(1024)
            if not buf:
                break
            checksum.update(buf)

    return checksum.hexdigest()


def print_dir_info(dir_name):
    total_times = list()

    for i in range(0, 5):
        total_time = 0

        total_files = 0
        total_bytes = 0

        for file in os.listdir(dir_name):
            full_filename = os.path.join(dir_name, file)
            if not os.path.isfile(full_filename):
                continue

            file_size = os.stat(full_filename).st_size

            start_time = time.perf_counter()
            md5 = get_file_checksum_md5_cached(full_filename)
            end_time = time.perf_counter()

            total_time += end_time - start_time

            total_files += 1
            total_bytes += file_size

            # print(f'{file}, {file_size} bytes ({bytes_to_human(file_size)}) MD5: {md5}')

        total_times.append(total_time)

        print(f'\n'
              f'Iteration #{i + 1}: {total_files} files, {total_bytes} bytes ({bytes_to_human(total_bytes)})')

    print(f"\n"
          f"Total time spent: {', '.join([f'{t:.06f}' for t in total_times])}")


def print_dir_info_2(dir_name):
    total_files = 0
    total_bytes = 0

    total_times = list()

    # prepare the same filenames 5x times
    filenames = list()

    for i in range(0, 5):
        for file in os.listdir(dir_name):
            full_filename = os.path.join(dir_name, file)
            if not os.path.isfile(full_filename):
                continue

            filenames.append(full_filename)

    random.shuffle(filenames)

    for filename in filenames:
        file_size = os.stat(filename).st_size

        start_time = time.perf_counter()
        md5 = get_file_checksum_md5(filename)
        end_time = time.perf_counter()

        total_times.append(end_time - start_time)

        total_files += 1
        total_bytes += file_size

        # print(f'{file}, {file_size} bytes ({bytes_to_human(file_size)}) MD5: {md5}')

    total_time = sum(total_times)

    print(f"\n"
          f"Total files: {total_files}, total bytes: {total_bytes} ({bytes_to_human(total_bytes)})\n"
          f"\n"
          f"Total time spent: {total_time:.02f} sec, avg. {total_files / total_time :.01f} files/sec\n")


if __name__ == '__main__':
    # print_dir_info('/Users/dipaolo/Downloads')
    print_dir_info_2('/Users/dipaolo/Downloads')
