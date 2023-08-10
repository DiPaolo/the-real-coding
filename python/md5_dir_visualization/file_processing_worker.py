import hashlib
import os
from enum import Enum

from PySide6.QtCore import QObject, Signal, Slot


class Type(Enum):
    SINGLE_THREAD = 1


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


def _process_file_single_thread(filename: str):
    checksum = None
    gen = _calc_file_checksum_md5(filename)
    while True:
        cur_file_pos, checksum = next(gen)
        # print(f'{ret}  {chesksum}')
        if cur_file_pos is None:
            break

        yield cur_file_pos, None

    yield None, checksum


class FileProcessingWorker(QObject):
    started = Signal()
    finished = Signal()
    progress = Signal(str, float)

    _cancel_requested = False
    _dir_name: str = None
    _type: Type = Type.SINGLE_THREAD
    _progress: float = 0.0

    def __init__(self, dir_name: str, type: Type = Type.SINGLE_THREAD):
        super().__init__()

        self._dir_name = dir_name
        self._type = type

    @property
    def total_progress(self) -> float:
        return self._progress

    def run(self):
        print('RUN')
        self.started.emit()

        print(len(os.listdir(self._dir_name)))

        for file in os.listdir(self._dir_name):
            # print(f'processing {file}...')
            if self._cancel_requested:
                break

            full_filename = os.path.join(self._dir_name, file)
            if not os.path.isfile(full_filename):
                continue

            file_size = os.stat(full_filename).st_size

            if self._type == Type.SINGLE_THREAD:
                gen = _process_file_single_thread(full_filename)

                cur_file_pos = 0
                calculated_value = None
                while not self._cancel_requested and calculated_value is None:
                    cur_file_pos, calculated_value = next(gen)
                    if cur_file_pos is None:
                        continue

                    progress = cur_file_pos * 100.0 / file_size
                    # print(f'{cur_file_pos}/{file_size} ({int(progress)}%) - {calculated_value}')
                    self.progress.emit(full_filename, progress)

                # print(f'------- {calculated_value} --------')
            else:
                # TODO handle error
                pass

        self.finished.emit()

    @Slot()
    def stop(self):
        self._cancel_requested = True
