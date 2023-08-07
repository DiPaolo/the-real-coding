import os
import random
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

from PySide6 import QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QWidget, QApplication


@dataclass
class FileInfo:
    full_filename: str
    size: int
    md5: Optional[str]
    rects: List[QRect]
    filled_rects: List[Tuple[QRect, QColor]]
    processing_progress: float


def get_file_infos(dir_name: str) -> List[FileInfo]:
    file_infos = list()

    for file in os.listdir(dir_name):
        if file.endswith('.sqlite'):
            continue

        full_filename = os.path.join(dir_name, file)
        if not os.path.isfile(full_filename):
            continue

        file_infos.append(FileInfo(full_filename, os.stat(full_filename).st_size, None, list(), list(),
                                   random.choice([random.randint(0, 80), 100])))

    return file_infos


class FileProcessingWidget(QWidget):
    def __init__(self, dir_name: str):
        super(FileProcessingWidget, self).__init__()

        self._cell_height = 12
        self._margin = 4  # 6
        self._indent = int(self._margin / 2)
        self._internal_height = self._cell_height - self._margin

        self._box_color = QColor(0xb9, 0xdb, 0x92)
        self._ready_color = self._box_color
        self._in_progress_color = QColor(0xff, 0xaa, 0x33)

        self._dir_name = dir_name
        self._file_infos = get_file_infos(self._dir_name)
        self._total_bytes = sum(fi.size for fi in self._file_infos)

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('MD5 Calculation')
        self.show()

    def paintEvent(self, event):
        rect = event.rect()
        print(rect)

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

            print(f'#{file_num}: name={fi.full_filename} size={fi.size} len_pix={file_len_pix}'
                  f'\t\t'
                  f'PROCESS: {fi.processing_progress:.02f}%')

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
                print(f'next line ({cur_line_num})')

            file_rects.append(QRect(next_start_pt.x(), next_start_pt.y(), pix_left, self._internal_height))
            if pix_processed_left > 0:
                fi.filled_rects.append((QRect(next_start_pt.x(), next_start_pt.y(), pix_processed_left,
                                              self._internal_height),
                                        self._in_progress_color if not file_is_ready else self._ready_color))

            next_start_pt.setX(next_start_pt.x() + pix_left + self._indent * 2)

            fi.rects = file_rects
            file_num += 1


def main():
    app = QApplication(sys.argv)
    DIR = '/Users/dipaolo/allure-report/history'
    DIR = '.'
    DIR = '/Users/dipaolo/Downloads'
    ex = FileProcessingWidget(DIR)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
