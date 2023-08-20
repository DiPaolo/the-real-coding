# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(910, 688)
        self.action_print = QAction(MainWindow)
        self.action_print.setObjectName(u"action_print")
        self.action_add = QAction(MainWindow)
        self.action_add.setObjectName(u"action_add")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 567, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_item = QPushButton(self.centralwidget)
        self.add_item.setObjectName(u"add_item")

        self.horizontalLayout_2.addWidget(self.add_item)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName(u"start")

        self.horizontalLayout_2.addWidget(self.start)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.stop = QPushButton(self.centralwidget)
        self.stop.setObjectName(u"stop")

        self.horizontalLayout_2.addWidget(self.stop)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.item_to_add_count = QSpinBox(self.centralwidget)
        self.item_to_add_count.setObjectName(u"item_to_add_count")
        self.item_to_add_count.setValue(10)

        self.horizontalLayout_2.addWidget(self.item_to_add_count)

        self.add_items = QPushButton(self.centralwidget)
        self.add_items.setObjectName(u"add_items")

        self.horizontalLayout_2.addWidget(self.add_items)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 910, 24))
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTools.menuAction())
        self.menuTools.addAction(self.action_print)
        self.menuTools.addAction(self.action_add)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"gui_multithreading_progress_visualization", None))
        self.action_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.action_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.add_item.setText(QCoreApplication.translate("MainWindow", u"Add One Item", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.add_items.setText(QCoreApplication.translate("MainWindow", u"Add Items", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
    # retranslateUi

