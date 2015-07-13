#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'

import wx
import logging
import os
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s'
)

ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class FileType:
    def __init__(self):
        self.pics = ['folder', 'file-python', 'file-unknown', 'up16']
        self.types = ['dir', 'python', 'unknown', 'up']
        picBasePath = 'images'
        self.picFiles = [
            os.path.join(picBasePath, "%s.png" % pic) for pic in self.pics
            ]
        print self.picFiles

    def GetIndex(self, type):
        try:
            index = self.types.index(type)
            return index
        except ValueError:
            return None


class FileListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
        self.log = logging.getLogger('MyTreeView')
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.path = None
        self.fileType = FileType()
        self.il = wx.ImageList(16, 16)
        for pic in self.fileType.picFiles:
            print pic
            self.il.Add(wx.Bitmap(pic))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self)

    def pop(self, path):
        self.path = path
        infos = self.GetFileInfos()

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

        if path == '/':
            # 已经位于根目录
            skipIndex = 0
        else:
            # 不是位于根目录，添加转到上级目录图标
            skipIndex = 1
            self.InsertStringItem(0, '..')
            self.SetItemImage(0, 3)

        for index, info in enumerate(infos):
            rowIndex = index + skipIndex
            self.InsertStringItem(rowIndex, info[0])
            self.SetStringItem(rowIndex, 1, info[1])
            self.SetStringItem(rowIndex, 2, "%s B"%info[2])
            self.SetStringItem(rowIndex, 3, info[3])
            self.SetItemImage(rowIndex, info[-1])

            if (rowIndex % 2) == 0:
                self.SetItemBackgroundColour(rowIndex, '#e6f1f5')

    def GetFileInfos(self):
        files = os.listdir(self.path)
        infos = [self.GetFileInfo(file) for file in files]
        return infos

    def GetFileInfo(self, filename):
        """
        Get file infomation
        :param
            filename: short filename
        :return
            list of filename like:
                [picindex, filename, ex, size, mod_time]
        """
        fullname = os.path.join(self.path, filename)

        (name, ext) = os.path.splitext(filename)
        ex = ext[1:]

        if os.path.isdir(fullname):
            picindex = self.fileType.GetIndex('dir')
            ex = '<dir>'
        elif ex == 'py':
            picindex = self.fileType.GetIndex('python')
        else:
            picindex = self.fileType.GetIndex('unknown')

        mod_time = os.path.getmtime(fullname)
        mod_time = time.strftime(self.time_format,
                                 time.localtime(mod_time))
        size = os.path.getsize(fullname)

        return [filename, ex, size, mod_time, picindex]

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print "OnItemSelected: %s, %s, %s, %s" % (self.currentItem,
                            self.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2))

        event.Skip()


class FileMouse(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        leftList = FileListCtrl(self.splitter, -1)
        rightList = FileListCtrl(self.splitter, -1)
        path1 = '.'
        path2 = '.'
        leftList.pop(path1)
        rightList.pop(path2)

        self.splitter.SplitVertically(leftList, rightList)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=ID_SPLITTER)

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER |
                                wx.TB_FLAT | wx.TB_TEXT)
        """
        tb.AddSimpleTool(10, wx.Bitmap('images/previous.png'), 'Previous')
        tb.AddSimpleTool(20, wx.Bitmap('images/up.png'), 'Up one directory')
        tb.AddSimpleTool(30, wx.Bitmap('images/home.png'), 'Home')
        tb.AddSimpleTool(40, wx.Bitmap('images/refresh.png'), 'Refresh')
        tb.AddSeparator()
        tb.AddSimpleTool(50, wx.Bitmap('images/write.png'), 'Editor')
        tb.AddSimpleTool(60, wx.Bitmap('images/terminal.png'), 'Terminal')
        tb.AddSeparator()
        tb.AddSimpleTool(70, wx.Bitmap('images/help.png'), 'Help')
        tb.Realize()
        """

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        button1 = wx.Button(self, ID_BUTTON + 1, "F3 View")
        button2 = wx.Button(self, ID_BUTTON + 2, "F4 Edit")
        button3 = wx.Button(self, ID_BUTTON + 3, "F5 Copy")
        button4 = wx.Button(self, ID_BUTTON + 4, "F6 Move")
        button5 = wx.Button(self, ID_BUTTON + 5, "F7 Mkdir")
        button6 = wx.Button(self, ID_BUTTON + 6, "F8 Delete")
        button7 = wx.Button(self, ID_BUTTON + 7, "F9 Rename")
        button8 = wx.Button(self, wx.ID_EXIT, "F10 Quit")

        self.sizer2.Add(button1, 1, wx.EXPAND)
        self.sizer2.Add(button2, 1, wx.EXPAND)
        self.sizer2.Add(button3, 1, wx.EXPAND)
        self.sizer2.Add(button4, 1, wx.EXPAND)
        self.sizer2.Add(button5, 1, wx.EXPAND)
        self.sizer2.Add(button6, 1, wx.EXPAND)
        self.sizer2.Add(button7, 1, wx.EXPAND)
        self.sizer2.Add(button8, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnExit, id=wx.ID_EXIT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        # 最大化
        # size = wx.DisplaySize()
        # self.SetSize(size)
        self.SetSize((800, 600))

        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText(os.getcwd())
        self.Center()
        self.Show(True)

    def OnExit(self, e):
        self.Close(True)

    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        self.sb.SetStatusText(os.getcwd())
        event.Skip()

    def OnDoubleClick(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)


app = wx.App(0)
FileMouse(None, -1, 'File Mouse')
app.MainLoop()
