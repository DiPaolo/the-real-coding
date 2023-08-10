import hashlib
import os

from PySide6.QtCore import QObject, Signal, Slot


class FileProcessingWorker(QObject):
    started = Signal()
    finished = Signal()
    # progress = Signal(float)

    _cancel_requested = False
    _filename: str = None
    _progress: float = 0.0

    def __init__(self, filename: str):
        super().__init__()

        self._filename = filename

    @property
    def progress(self) -> float:
        return self._progress

    def run(self):
        self.started.emit()

        for file in os.listdir(self._filename):
            if self._cancel_requested:
                break

            full_filename = os.path.join(self._filename, file)
            if not os.path.isfile(full_filename):
                continue

            file_size = os.stat(full_filename).st_size

            checksum = hashlib.md5()
            with open(full_filename, 'rb') as f:
                while not self._cancel_requested:
                    buf = f.read(1024)
                    if not buf:
                        break
                    checksum.update(buf)

                    self._progress = f.tell() * 100.0 / file_size

            md5 = checksum.hexdigest()

        self.finished.emit()

    @Slot()
    def stop(self):
        self._cancel_requested = True
