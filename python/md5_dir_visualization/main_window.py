import os.path
from typing import List

from PySide6.QtCore import Slot, QStandardPaths
from PySide6.QtWidgets import QMainWindow, QFileDialog

from python.md5_dir_visualization import settings
from python.md5_dir_visualization.settings import SettingsKey
from python.md5_dir_visualization.ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    _thread = None
    _worker = None

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # restore position and state
        # self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))

        # connections
        # self.ui.start.clicked.connect(self._start)
        # self.ui.stop.clicked.connect(self._stop)
        self.ui.recent_dirs.currentIndexChanged.connect(self._on_current_dir_changed)
        self.ui.choose_dir.clicked.connect(self._choose_dir)

        # initial UI setup; after connections are made!!!
        # self.ui.progress.setText('not started')
        # self.ui.start.setEnabled(True)
        # self.ui.stop.setEnabled(False)
        recent_dirs = settings.get_settings_list_value(SettingsKey.RECENT_CHOSEN_DIRS)
        for cur_dir in recent_dirs:
            self.ui.recent_dirs.addItem(cur_dir)

    def closeEvent(self, event):
        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY, self.saveGeometry())
        # settings.set_settings_byte_array_value(SettingsKey.WINDOW_STATE, self.windowState())

    @Slot()
    def _on_current_dir_changed(self, idx: int):
        recent_dirs = self._get_recent_dirs_from_combo()

        # move the currently chosen dir to the top
        cur_dir = self.ui.recent_dirs.itemText(idx)
        recent_dirs.remove(cur_dir)
        recent_dirs.insert(0, cur_dir)

        # to avoid infinite slot calls
        self.ui.recent_dirs.currentIndexChanged.disconnect()

        self.ui.recent_dirs.clear()
        for d in recent_dirs:
            self.ui.recent_dirs.addItem(d)

        self.ui.recent_dirs.setCurrentIndex(0)

        # connect it back
        self.ui.recent_dirs.currentIndexChanged.connect(self._on_current_dir_changed)

        # update settings
        settings.set_settings_list_value(SettingsKey.RECENT_CHOSEN_DIRS, self._get_recent_dirs_from_combo())

        self.ui.file_processing_widget.set_dir(cur_dir)

    @Slot()
    def _choose_dir(self):
        recent_dirs = settings.get_settings_list_value(SettingsKey.RECENT_CHOSEN_DIRS)
        open_folder = recent_dirs[0] if len(recent_dirs) else QStandardPaths.standardLocations(
            QStandardPaths.StandardLocation.HomeLocation)[0]

        dir_path = QFileDialog.getExistingDirectory(self, 'Choose Directory', open_folder)
        if not dir_path:
            return

        dir_path = os.path.abspath(dir_path)
        if self.ui.recent_dirs.findText(dir_path) != -1:
            return

        self.ui.recent_dirs.insertItem(0, dir_path)
        self.ui.recent_dirs.setCurrentIndex(0)

        settings.set_settings_list_value(SettingsKey.RECENT_CHOSEN_DIRS, self._get_recent_dirs_from_combo())

    # @Slot()
    # def _start(self):
    #     self._stop()
    #
    #     self._thread = QThread()
    #     self._worker = FileProcessingWorker(self.ui.recent_dirs.currentText())
    #     self._worker.moveToThread(self._thread)
    #
    #     self._thread.started.connect(self._worker.run)
    #     self._worker.started.connect(self._on_started)
    #     self._worker.finished.connect(self._on_finished)
    #     # self._worker.progress.connect(self._update_progress)
    #
    #     self._thread.start()
    #
    # @Slot()
    # def _stop(self):
    #     if self._worker is not None:
    #         print('self._worker.stop()')
    #         self._worker.stop()
    #         print('self._worker = None')
    #         self._worker.deleteLater()
    #         self._worker = None
    #
    #     if self._thread is not None:
    #         print('self._thread.quit()')
    #         self._thread.quit()
    #         print('self._thread.wait()')
    #         self._thread.wait()
    #         print('self._thread = None')
    #         self._thread.deleteLater()
    #         self._thread = None

    @Slot()
    def _update_progress(self, progress: int):
        self.ui.statusbar.setText(f'{progress:.1f}%')

    @Slot()
    def _on_started(self):
        # self.ui.start.setEnabled(False)
        # self.ui.stop.setEnabled(True)
        pass

    @Slot()
    def _on_finished(self):
        # self.ui.start.setEnabled(True)
        # self.ui.stop.setEnabled(False)
        pass

    def _get_recent_dirs_from_combo(self) -> List[str]:
        recent_dirs = list()
        for i in range(0, self.ui.recent_dirs.count()):
            recent_dirs.append(self.ui.recent_dirs.itemText(i))

        return recent_dirs
