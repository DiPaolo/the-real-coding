import random

from PySide6.QtCore import Slot, QThread, Signal
from PySide6.QtWidgets import QWidget

from .file_processing_worker import FileProcessingWorker
from .ui.ui_processing_item_widget import Ui_Form


class ProcessingItemWidget(QWidget):
    started = Signal()
    finished = Signal()

    _thread = None
    _worker = None

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # initial UI setup
        self.ui.progress.setText('not started')

    def __del__(self):
        self.stop(True)

    def is_running(self) -> bool:
        return self._thread.isRunning() if self._thread else False

    @Slot()
    def start(self):
        self.stop()

        self._thread = QThread()
        self._worker = FileProcessingWorker(random.randint(1, 30))
        self._worker.moveToThread(self._thread)
        self._worker.started.connect(self.started)
        self._worker.finished.connect(self.stop)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._update_progress)

        self._thread.start()

    @Slot()
    def stop(self, cleanup=False):
        if self._worker is not None:
            self._worker.stop()
            self._worker = None

        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread = None

        # signal object is already deleted if called from __del__()
        if not cleanup:
            self.finished.emit()

    @Slot()
    def _update_progress(self, progress: float):
        self.ui.progress.setText(f'{progress:.1f}%')
        self.ui.progress_bar.setValue(progress)
