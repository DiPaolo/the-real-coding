import os

from PySide6 import QtGui
from PySide6.QtCore import QRect, QPoint, Slot, QThread, Signal
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QWidget

from python.md5_dir_visualization.file_info import get_file_infos
from python.md5_dir_visualization.file_processing_worker import FileProcessingWorker


class FileProcessingWidget(QWidget):
    started = Signal()
    finished = Signal()

    _thread = None
    _worker = None
    _cancel_requested = False

    def __init__(self, parent: QWidget):
        super(FileProcessingWidget, self).__init__(parent)

        self._cell_height = 12
        self._margin = 4  # 6
        self._indent = int(self._margin / 2)
        self._internal_height = self._cell_height - self._margin

        self._box_color = QColor(0xb9, 0xdb, 0x92)
        self._ready_color = self._box_color
        self._in_progress_color = QColor(0xff, 0xaa, 0x33)

        self._dir_name = ''
        self._file_infos = list()
        self._total_bytes = 0

        self.set_dir('')

    def set_dir(self, dir_name: str):
        self._dir_name = dir_name
        self._file_infos = get_file_infos(self._dir_name)
        self._total_bytes = sum(fi.size for fi in self._file_infos)

        self._calc_spans(QRect(QPoint(0, 0), self.size()))
        self.repaint()

    def paintEvent(self, event):
        rect = event.rect()
        # print(rect)

        qp = QtGui.QPainter()
        qp.begin(self)

        pen = QPen(self._box_color)
        pen.setWidth(0)
        qp.setPen(pen)

        for fi in self._file_infos:
            for r in fi.rects:
                qp.drawRect(r)

            for r in fi.filled_rects:
                qp.fillRect(r[0], r[1])

        qp.end()

    def resizeEvent(self, event):
        self._calc_spans(QRect(QPoint(0, 0), event.size()))

    @Slot()
    def start(self):
        for fi in self._file_infos:
            full_filename = fi.full_filename
            if not os.path.isfile(full_filename):
                continue

            self._start_process_file(full_filename)

    @Slot()
    def _start_process_file(self, filename: str):
        self._stop_process_file()

        self._thread = QThread()
        self._worker = FileProcessingWorker(filename)
        self._worker.moveToThread(self._thread)
        self._worker.started.connect(self.started)
        self._worker.finished.connect(self._stop_process_file)

        self._thread.started.connect(self._worker.run)
        # self._worker.progress.connect(self._update_progress)

        self._thread.start()

    @Slot()
    def stop(self, cleanup=False):
        pass

    @Slot()
    def _stop_process_file(self, cleanup=False):
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

    def _calc_spans(self, window_rect: QRect):
        rows = window_rect.height() // self._cell_height

        # calculate number of bytes per 1pix
        row_len_pix = window_rect.width() - self._indent * 2
        total_strip_len = rows * row_len_pix
        bytes_per_pix = self._total_bytes / total_strip_len

        file_num = 0
        cur_line_num = 0
        next_start_pt = window_rect.topLeft() + QPoint(self._indent, self._indent)
        for fi in self._file_infos:
            file_len_pix = max(fi.size / bytes_per_pix, 1)
            file_processing_status_pix = file_len_pix * fi.processing_progress / 100.0

            file_is_ready = fi.processing_progress >= 100.0

            # print(f'#{file_num}: name={fi.full_filename} size={fi.size} len_pix={file_len_pix}'
            #       f'\t\t'
            #       f'PROCESS: {fi.processing_progress:.02f}%')

            file_rects = list()
            pix_left = file_len_pix
            pix_processed_left = file_processing_status_pix
            cur_line_len_pix = window_rect.width() - next_start_pt.x() - self._indent
            while pix_left >= cur_line_len_pix:
                file_rects.append(QRect(next_start_pt.x(), next_start_pt.y(), cur_line_len_pix, self._internal_height))

                if pix_processed_left > 0:
                    reduce_by_pix = min(pix_processed_left, cur_line_len_pix)
                    fi.filled_rects.append((QRect(next_start_pt.x(), next_start_pt.y(), reduce_by_pix,
                                                  self._internal_height),
                                            self._in_progress_color if not file_is_ready else self._ready_color))
                    pix_processed_left -= reduce_by_pix

                next_start_pt.setX(self._indent)
                next_start_pt.setY(next_start_pt.y() + self._cell_height)
                pix_left -= cur_line_len_pix
                cur_line_len_pix = window_rect.width() - next_start_pt.x() - self._indent
                cur_line_num += 1
                # print(f'next line ({cur_line_num})')

            file_rects.append(QRect(next_start_pt.x(), next_start_pt.y(), pix_left, self._internal_height))
            if pix_processed_left > 0:
                fi.filled_rects.append((QRect(next_start_pt.x(), next_start_pt.y(), pix_processed_left,
                                              self._internal_height),
                                        self._in_progress_color if not file_is_ready else self._ready_color))

            next_start_pt.setX(next_start_pt.x() + pix_left + self._indent * 2)

            fi.rects = file_rects
            file_num += 1
