#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:         run.py
# Purpose:      file manager with two columns
# Created:      2015-06-28
# LastModify    2017-03-31
# Copyright:    Dormouse.Young
# Licence:      GPL V3.0
# ---------------------------------------------------------------------------
import sys

from PyQt5.QtCore import (QSize)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QVBoxLayout, QHBoxLayout)

from run import FileView

__author__ = 'Dormouse Young'
__version__ = '0.1'


class TestFileWin(QWidget):
    def __init__(self):
        super(TestFileWin, self).__init__()
        self.file_win = FileView('/tmp')

        button_layout = QHBoxLayout()
        button_get_selected_paths = QPushButton("get_selected_paths")
        button_col_widths = QPushButton("cols width")
        button_layout.addWidget(button_get_selected_paths)
        button_layout.addWidget(button_col_widths)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.file_win)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        # self.setCentralWidget(main_layout)
        self.resize(QSize(800, 600))

        button_get_selected_paths.clicked.connect(self.get_selected_paths)
        button_col_widths.clicked.connect(self.col_widths)

    def get_selected_paths(self):
        print(self.file_win.get_selected_paths())

    def col_widths(self):
        print(self.file_win.get_col_widths())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TestFileWin()
    mainWin.show()
    sys.exit(app.exec_())
