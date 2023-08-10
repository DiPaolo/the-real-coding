import hashlib
import os
from enum import Enum
from typing import List

from python.md5_dir_visualization.file_info import FileInfo


class Type(Enum):
    SINGLE_THREAD = 1


def process_files(file_infos: List[FileInfo], type: Type):
    for fi in file_infos:
        full_filename = fi.full_filename
        if not os.path.isfile(full_filename):
            continue

        if type == Type.SINGLE_THREAD:
            process_file_single_thread(full_filename)
        else:
            # TODO handle error
            pass


def process_file_single_thread(filename: str):
    gen = _calc_file_checksum_md5(filename)
    while True:
        ret, checksum = next(gen)
        # print(f'{ret}  {chesksum}')
        if ret is None:
            break



def _calc_file_checksum_md5(filename: str):
    checksum = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            buf = f.read(1024)
            if not buf:
                break
            checksum.update(buf)
            yield f.tell(), None

    yield None, checksum.hexdigest()
