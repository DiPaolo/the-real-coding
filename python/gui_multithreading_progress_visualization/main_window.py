import random

from PySide6.QtCore import Slot, QThread
from PySide6.QtWidgets import QMainWindow

from .file_processing_worker import FileProcessingWorker
from .ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    _thread = None
    _worker = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # initial UI setup
        self.ui.progress.setText('not started')
        self.ui.start.setEnabled(True)
        self.ui.stop.setEnabled(False)

        # connections
        self.ui.start.clicked.connect(self._start)
        self.ui.stop.clicked.connect(self._stop)

    def __del__(self):
        self._stop()

    @Slot()
    def _start(self):
        self._stop()

        self._thread = QThread()
        self._worker = FileProcessingWorker(random.randint(4, 15))
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.started.connect(self._on_started)
        self._worker.finished.connect(self._on_finished)
        self._worker.progress.connect(self._update_progress)

        self._thread.start()

    @Slot()
    def _stop(self):
        if self._worker is not None:
            print('self._worker.stop()')
            self._worker.stop()
            print('self._worker = None')
            self._worker = None

        if self._thread is not None:
            print('self._thread.quit()')
            self._thread.quit()
            print('self._thread.wait()')
            self._thread.wait()
            print('self._thread = None')
            self._thread = None

    @Slot()
    def _update_progress(self, progress: float):
        self.ui.progress.setText(f'{progress:.1f}%')
        self.ui.progress_bar.setValue(progress)

    @Slot()
    def _on_started(self):
        self.ui.start.setEnabled(False)
        self.ui.stop.setEnabled(True)

    @Slot()
    def _on_finished(self):
        self.ui.start.setEnabled(True)
        self.ui.stop.setEnabled(False)
