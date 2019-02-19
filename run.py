#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:         run.py
# Purpose:      file manager with two columns
# Created:      2015-06-28
# LastModify    2019-01-21
# Copyright:    Dormouse.Young
# Licence:      GPL V3.0
# ---------------------------------------------------------------------------
import logging
import os
import sys
import subprocess
from pathlib import Path
from PyQt5.QtCore import (QEvent, QPoint, QSignalMapper, QSize, Qt)
from PyQt5.QtGui import (QFont, QIcon, QKeySequence)
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMdiArea,
                             QMessageBox, QWidget, QSplitter, QTreeView,
                             QListView, QTableView, QAbstractItemView,
                             QFileSystemModel, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QDockWidget)
from helper.option import Option
from commands import core
from functools import partial

__author__ = 'Dormouse Young'
__version__ = '0.1'

from project_conf import DEBUG
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.WARNING

logging.basicConfig(
    format='%(asctime)s %(module)s %(funcName)s %(levelname)s %(message)s',
    level=level
)


class FileView(QWidget):
    def __init__(self, root_path='.'):
        super(FileView, self).__init__()
        self.logger = logging.getLogger(__name__)
        if not Path(root_path).exists():
            root_path = '.'
        self.view = QTableView()
        self.view.installEventFilter(self)
        self.model = QFileSystemModel(self.view)
        self.root_path_widget = QLineEdit()
        self.go_up_button = QPushButton("..")
        self.go_up_button.setMaximumWidth(30)
        self.model.setReadOnly(False)

        self.view.setModel(self.model)
        self.view.verticalHeader().setHidden(True)  # 隐藏纵向表头
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)  # 选择时选择整行
        self.view.setAlternatingRowColors(True)  # 行间变色
        self.view.setShowGrid(False)  # 隐藏表格线
        self.view.setSortingEnabled(True)  # 开启表头排序

        root_index = self.model.setRootPath(root_path)
        self.view.setRootIndex(root_index)
        self.root_path_changed(root_path)

        # 组装控件
        layout_up = QHBoxLayout()
        layout_up.addWidget(self.root_path_widget)
        layout_up.addWidget(self.go_up_button)
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_up)
        layout_main.addWidget(self.view)
        self.setLayout(layout_main)

        # connect signals
        self.view.doubleClicked.connect(self.view_double_clicked)
        self.model.rootPathChanged.connect(self.root_path_changed)
        self.go_up_button.clicked.connect(self.go_up_button_clicked)

        self.view.setFocus()
        self.is_activate = True

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            self.nativeParentWidget().activate(self)
        elif event.type() == QEvent.FocusOut:
            pass
            # self.not_highlight_root_path_widget()
            # self.view.clearSelection()
            # self.is_activate = False

            # if obj == self.view:
            #     print("view")
            # elif obj == self.root_path_widget:
            #     print("root path widget")
            # elif obj == self.go_up_button:
            #     print("go up button")
        return super(FileView, self).eventFilter(obj, event)

    # def focusInEvent(self, evt):
    #     self.highlight_root_path_widget()
    #
    # def focusOutEvent(self, evt):
    #     self.not_highlight_root_path_widget()

    def get_selected_paths(self):
        """
        get all selected paths
        :return: None or a list of paths
        """
        indexes = self.view.selectedIndexes()
        if indexes:
            first_col_indexes = list(filter(
                lambda x:x.column()==0, indexes
            ))
            paths = [
                self.model.fileInfo(index).absoluteFilePath()
                for index in first_col_indexes
            ]
            return paths
        else:
            return None

    def get_selected_file(self):
        paths = self.get_selected_paths()
        if paths and len(paths) == 1 and Path(paths[0]).is_file():
            return paths[0]
        else:
            return None

    def get_col_widths(self):
        """
        get width of all cols
        :return: a list of width of all cols
        """
        col_counts = self.model.columnCount()
        return [self.view.columnWidth(i) for i in range(col_counts)]

    def go_up_button_clicked(self):
        current_root_path = self.model.rootPath()
        abs_path = Path(current_root_path).absolute()
        root_index = self.model.setRootPath(str(abs_path.parent))
        self.view.setRootIndex(root_index)

    def root_path_changed(self, path):
        self.logger.debug(f"root path changed to:{path}")
        abs_path = Path(path).absolute()
        # root = self.model.setRootPath(path)
        # self.view.setRootIndex(root)
        # self.view.setRootIndex(self.model.index(self.model.rootPath()))

        # 显示 ROOT 路径的控件
        self.root_path_widget.setText(str(abs_path))
        self.root_path_widget.setReadOnly(True)

        # 设置窗口标题（TAB的标题）
        self.setWindowTitle(abs_path.stem)
        self.view.setFocus()

    def view_double_clicked(self, index):
        if not index.isValid():
            return
        abs_path = self.model.fileInfo(index).absoluteFilePath()
        if self.model.fileInfo(index).isDir():
            root_index = self.model.setRootPath(abs_path)
            self.view.setRootIndex(root_index)
        else:
            self.logger.debug(f"view {abs_path}")

    def highlight_root_path_widget(self):
        self.root_path_widget.setStyleSheet(
            "background-color:rgba(0,255,255,255)")

    def not_highlight_root_path_widget(self):
        self.root_path_widget.setStyleSheet(
            "background-color:rgba(255,255,255,255)")


class HalfWindow(QMainWindow):
    def __init__(self, root_path='.'):
        super(HalfWindow, self).__init__()
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.setCentralWidget(self.mdiArea)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.set_active_sub_window)
        self.file_tree = FileView(root_path)
        self.new_child(self.file_tree)
        self.file_tree.showMaximized()

    def set_active_sub_window(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def new_child(self, child):
        self.mdiArea.addSubWindow(child)
        child.show()


class CmdButtonBox(QWidget):
    def __init__(self):
        super(CmdButtonBox, self).__init__()
        main_layout = QHBoxLayout()
        buttons = {
            "f3": "F3 查看",
            "f4": "F4 编辑",
            "f5": "F5 复制",
            "f6": "F6 移动",
            "f7": "F7 新建文件夹",
            "f8": "F8 删除",
        }
        button_widgets = {}
        for k, v in buttons.items():
            button_widgets[k] = QPushButton(v)
            button_widgets[k].clicked.connect(partial(self.cmd, k))
            main_layout.addWidget(button_widgets[k])
        self.setLayout(main_layout)

    def cmd(self, cmd_str):
        self.nativeParentWidget().cmd(cmd_str)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.sp = QSplitter(self)
        op = Option()
        self.left_win = HalfWindow(op.root_path_left)
        self.right_win = HalfWindow(op.root_path_right)
        self.sp.addWidget(self.left_win)
        self.sp.addWidget(self.right_win)

        self.cmd_button_box = CmdButtonBox()

        vbox = QVBoxLayout()
        vbox.addWidget(self.sp)
        vbox.addWidget(self.cmd_button_box)

        self.setLayout(vbox)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.main_widget = MainWidget()
        self.actions = {}
        self.setCentralWidget(self.main_widget)
        self.createActions()
        self.createMenus()
        self.read_settings()
        self.setWindowTitle("File Mouse")

        self.activated_view = None
        self.deactivated_view = None
        self.left_view = self.main_widget.left_win.file_tree
        self.right_view = self.main_widget.right_win.file_tree
        self.activate(self.left_view)

    def activate(self, fileview):
        self.activated_view = fileview
        if fileview == self.left_view:
            self.deactivated_view = self.right_view
        else:
            self.deactivated_view = self.left_view

        self.activated_view.highlight_root_path_widget()
        self.deactivated_view.not_highlight_root_path_widget()
        self.deactivated_view.view.clearSelection()

    def about(self):
        QMessageBox.about(
            self,
            "About",
            "<b>File Mouse</b>"
            "A File manager with two columns."
        )

    def closeEvent(self, event):
        for win in [self.main_widget.left_win, self.main_widget.right_win]:
            win.mdiArea.closeAllSubWindows()
        if self.main_widget.left_win.mdiArea.currentSubWindow() or \
                self.main_widget.right_win.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.wrtie_settings()
            event.accept()

    def cmd(self, cmd):
        self.logger.debug(f"{cmd}")
        if cmd == 'f3':
            path = self.activated_view.get_selected_file()
            if path:
                core.cmd_view(path)
        elif cmd == 'f4':
            path = self.activated_view.get_selected_file()
            if path:
                core.cmd_edit(path)
        elif cmd == 'f5':
            source = self.activated_view.get_selected_paths()
            target = self.deactivated_view.model.rootPath()
            self.logger.debug(source)
            self.logger.debug(target)



    def createActions(self):
        self.exitAct = QAction(
            "退出(&X)", self,
            shortcut=QKeySequence.Quit,
            statusTip="退出",
            triggered=QApplication.instance().closeAllWindows
        )
        self.aboutAct = QAction(
            "关于(&A)", self,
            shortcut=Qt.Key_F1,
            statusTip="显示本系统的说明信息",
            triggered=self.about
        )
        self.aboutQtAct = QAction(
            "关于 &Qt", self,
            statusTip="显示 Qt 库的说明信息",
            triggered=QApplication.instance().aboutQt
        )

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("文件(&F)")
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("帮助(&H)")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def read_settings(self):
        op = Option()
        globe = op.globe
        self.move(QPoint(globe.x, globe.y))
        self.resize(QSize(globe.width, globe.height))

    def wrtie_settings(self):
        """ 保存设置 """
        op = Option()
        globe = op.globe
        pos = self.pos()
        globe.x = pos.x()
        globe.y = pos.y()
        size = self.size()
        globe.width = size.width()
        globe.height = size.height()

        op.root_path_left = self.left_view.model.rootPath()
        op.root_path_right = self.right_view.model.rootPath()
        op.save()

    def get_activate_file_view(self):
        left_view = self.main_widget.left_win.file_tree
        right_view = self.main_widget.right_win.file_tree
        if left_view.is_activate:
            return left_view
        else:
            return right_view

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F3:
            self.cmd('f3')
        if evt.key() == Qt.Key_F4:
            self.cmd('f4')
        return super(MainWindow, self).keyPressEvent(evt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
