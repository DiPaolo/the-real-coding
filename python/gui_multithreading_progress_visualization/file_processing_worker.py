import time

from PySide6.QtCore import QObject, Signal, Slot


class FileProcessingWorker(QObject):
    started = Signal()
    finished = Signal()
    progress = Signal(float)

    _cancel_requested = False
    _duration: float = 0.0

    def __init__(self, duration: int):
        super().__init__()

        self._duration = duration

    def run(self):
        spent_time = 0.0
        start_time = time.perf_counter()

        self.started.emit()

        while not self._cancel_requested and spent_time < self._duration:
            time.sleep(0.1)
            spent_time = time.perf_counter() - start_time
            self.progress.emit(min(spent_time * 100.0 / self._duration, 100.0))

        self.finished.emit()

    @Slot()
    def stop(self):
        self._cancel_requested = True
