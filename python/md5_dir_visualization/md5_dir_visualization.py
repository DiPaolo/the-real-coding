import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from python.md5_dir_visualization.file_processing_widget import FileProcessingWidget
from python.md5_dir_visualization.main_window import MainWindow


def main():
    QCoreApplication.setOrganizationName('DiPaolo')
    QCoreApplication.setOrganizationDomain('dipaolo.dev')
    QCoreApplication.setApplicationName('MD5 for Directory Visualization')

    app = QApplication(sys.argv)
    DIR = '/Users/dipaolo/allure-report/history'
    DIR = '.'
    DIR = '/Users/dipaolo/Downloads'
    # ex = FileProcessingWidget(DIR)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
