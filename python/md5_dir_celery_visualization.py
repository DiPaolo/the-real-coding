import os
import sys
from typing import Dict, List

from PySide6 import QtGui
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QApplication


def get_file_infos(dir_name: str) -> Dict[str, int]:
    file_infos = dict()

    for file in os.listdir(dir_name):
        if file.endswith('.sqlite'):
            continue

        full_filename = os.path.join(dir_name, file)
        if not os.path.isfile(full_filename):
            continue

        file_infos[full_filename] = os.stat(full_filename).st_size

    return file_infos


class FileProcessingWidget(QWidget):
    def __init__(self, dir_name: str):
        super(FileProcessingWidget, self).__init__()

        # cell_size = 12  # 16
        # cell_width = 12
        self._cell_height = 12
        self._margin = 4  # 6
        self._indent = int(self._margin / 2)
        # internal_size = cell_size - margin
        # internal_width = cell_width - margin
        self._internal_height = self._cell_height - self._margin

        self._dir_name = dir_name
        self._file_infos = get_file_infos(self._dir_name)
        self._total_bytes = sum(fi for _, fi in self._file_infos.items())

        self._spans = None

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('MD5 Calculation')
        self.show()

    def paintEvent(self, event):
        rect = event.rect()
        print(rect)

        qp = QtGui.QPainter()
        qp.begin(self)

        qp.setPen(QColor(0xb9, 0xdb, 0x92))
        # qp.setBrush(QBrush(QColor(0xb9, 0xdb, 0x92)))

        for span in self._spans:
            qp.drawRect(span)

        qp.end()

    def resizeEvent(self, event):
        self._spans = self._calc_spans(QRect(QPoint(0, 0), event.size()))

    def _calc_spans(self, window_rect: QRect) -> List[QRect]:
        out = list()

        rows = window_rect.height() // self._cell_height

        # calculate number of bytes per 1pix
        row_len_pix = window_rect.width() - self._indent * 2
        total_strip_len = rows * row_len_pix
        bytes_per_pix = self._total_bytes / total_strip_len

        file_num = 0
        cur_line_num = 0
        next_start_pt = window_rect.topLeft() + QPoint(self._indent, self._indent)
        for filename, file_size in self._file_infos.items():
            file_len_pix = file_size / bytes_per_pix

            print(f'#{file_num}: name={filename} size={file_size} len_pix={file_len_pix}')

            pix_left = file_len_pix
            cur_line_len_pix = window_rect.width() - next_start_pt.x() - self._indent
            while pix_left >= cur_line_len_pix:
                out.append(QRect(next_start_pt.x(), next_start_pt.y(), cur_line_len_pix, self._internal_height))
                next_start_pt.setX(self._indent)
                next_start_pt.setY(next_start_pt.y() + self._cell_height)
                pix_left -= cur_line_len_pix
                cur_line_len_pix = window_rect.width() - next_start_pt.x() - self._indent
                cur_line_num += 1
                print(f'next line ({cur_line_num})')

            out.append(QRect(next_start_pt.x(), next_start_pt.y(), pix_left, self._internal_height))
            next_start_pt.setX(next_start_pt.x() + pix_left + self._indent * 2)

            file_num += 1

        return out


def main():
    app = QApplication(sys.argv)
    DIR = '/Users/dipaolo/allure-report/history'
    DIR = '.'
    DIR = '/Users/dipaolo/Downloads'
    ex = FileProcessingWidget(DIR)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
