import sys

from PySide6.QtWidgets import QApplication

from python.gui_multithreading_progress_visualization.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
