from typing import List

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

from .processing_item_widget import ProcessingItemWidget
from .ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    _thread = None
    _worker = None

    _col_count = 10

    _cur_item_row = 0
    _cur_item_col = 0
    _processing_items: List[List[ProcessingItemWidget]] = [[]]

    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._update_buttons()

        # connections
        self.ui.action_print.triggered.connect(self._print_grid_info)
        self.ui.action_add.triggered.connect(self._add_item)

        self.ui.add_item.clicked.connect(self._add_item)
        self.ui.start.clicked.connect(self._start)
        self.ui.stop.clicked.connect(self._stop)
        self.ui.add_items.clicked.connect(lambda: self._add_items(self.ui.item_to_add_count.value()))

    def __del__(self):
        self._stop()

    @Slot()
    def _print_grid_info(self):
        print('\n'
              '\n')
        for i in range(0, self.ui.gridLayout.rowCount()):
            for j in range(0, self.ui.gridLayout.columnCount()):
                print(f'{i}, {j}: {self.ui.gridLayout.itemAtPosition(i, j)}')

    @Slot()
    def _add_item(self):
        next_row = self._cur_item_row
        next_col = self._cur_item_col + 1
        if next_col == self._col_count:
            next_row += 1
            next_col = 0

        # is new row
        if self._cur_item_col == 0:
            # yes; move vertical spacer and start/stop buttons one row down

            new_buttons_row = self.ui.gridLayout.rowCount()
            old_spacer_row = self.ui.gridLayout.rowCount() - 2
            new_spacer_row = new_buttons_row - 1
            spacer_col = 1

            # buttons
            self.ui.gridLayout.removeItem(self.ui.horizontalLayout_2)
            self.ui.gridLayout.addLayout(self.ui.horizontalLayout_2, new_buttons_row, 0, 1, self._col_count)

            # spacer
            self.ui.gridLayout.removeItem(self.ui.gridLayout.itemAtPosition(old_spacer_row, spacer_col))
            self.ui.gridLayout.addItem(self.ui.verticalSpacer, new_spacer_row, spacer_col)

            # make spacer maximum extendable
            self.ui.gridLayout.setRowStretch(old_spacer_row, 0)
            self.ui.gridLayout.setRowStretch(new_spacer_row, 1)

        new_item = ProcessingItemWidget(self.ui.centralwidget)
        new_item.started.connect(self._update_buttons)
        new_item.finished.connect(self._update_buttons)

        self.ui.gridLayout.addWidget(new_item, self._cur_item_row, self._cur_item_col)

        # add item to matrix of objects
        if self._cur_item_col == 0:
            self._processing_items.append(list())

        self._processing_items[self._cur_item_row].append(new_item)

        self._cur_item_row = next_row
        self._cur_item_col = next_col

        self._update_buttons()

    # @Slot()
    def _add_items(self, n: int):
        for i in range(0, n):
            self._add_item()

    @Slot()
    def _start(self):
        self._stop()

        for row in self._processing_items:
            for proc_item in row:
                proc_item.start()

    @Slot()
    def _stop(self):
        for row in self._processing_items:
            for proc_item in row:
                proc_item.stop()

    @Slot()
    def _update_buttons(self):
        at_least_one_item = False
        is_running = False
        for row in self._processing_items:
            for proc_item in row:
                at_least_one_item = True
                if proc_item.is_running():
                    is_running = True

        self.ui.start.setEnabled(not is_running and at_least_one_item)
        self.ui.stop.setEnabled(is_running)
