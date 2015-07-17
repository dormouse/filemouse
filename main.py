#!/usr/bin/python
# -*- coding: utf8 -*-

# Create:   2015-07-09
# Modify:   2015-07-16
# Author:   Dormouse Young
# Email:    dormouse dot young at gmail dot com
# Licence:  GPLv3

# Todo:
#

# History:
#
#

# Knowing bug:
# 1. If no dir in path, will not select default item


__author__ = 'dormouse'
__version__ = '0.1'

import wx
import logging
import os
import shutil
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s'
)

ID_BUTTON = wx.NewId()
ID_BUTTON_VIEW = wx.NewId()
ID_BUTTON_COPY = wx.NewId()
ID_SPLITTER = wx.NewId()
ID_LEFTLIST = wx.NewId()
ID_RIGHTLIST = wx.NewId()


class FileType:
    def __init__(self):
        self.pics = ['folder', 'file-python', 'file-unknown', 'up16']
        self.types = ['dir', 'python', 'unknown', 'up']
        picBasePath = 'images'
        self.picFiles = [
            os.path.join(picBasePath, "%s.png" % pic) for pic in self.pics
            ]

    def GetIndex(self, type):
        try:
            index = self.types.index(type)
            return index
        except ValueError:
            return None


class FileListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.log = logging.getLogger('FileListCtrl')
        self.mainWin = self.GetTopLevelParent()
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.path = None
        self.fileType = FileType()
        self.il = wx.ImageList(16, 16)
        for pic in self.fileType.picFiles:
            self.il.Add(wx.Bitmap(pic))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def pop(self, path):
        self.path = os.path.abspath(path)
        infos = self.GetFileInfos()

        self.ClearAll()
        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

        if self.path == '/':
            # 已经位于根目录
            defaultItem = 0
        else:
            # 不是位于根目录，添加转到上级目录图标
            defaultItem = 1
            self.InsertStringItem(0, '..')
            self.SetItemImage(0, 3)
        self.log.debug("default item:%s", defaultItem)
        for index, info in enumerate(infos):
            rowIndex = index + defaultItem
            self.InsertStringItem(rowIndex, info[0])
            self.SetStringItem(rowIndex, 1, info[1])
            self.SetStringItem(rowIndex, 2, "%s B" % info[2])
            self.SetStringItem(rowIndex, 3, info[3])
            self.SetItemImage(rowIndex, info[-1])

            if (rowIndex % 2) == 0:
                self.SetItemBackgroundColour(rowIndex, '#e6f1f5')

        # self.UnSelectAll()
        # set default selected item
        # self.Select(defaultItem)
        # self.SetItemState(defaultItem,
        #                   wx.LIST_STATE_SELECTED,
        #                   wx.LIST_STATE_SELECTED)
        self.mainWin.sb.SetStatusText(self.path)

    def UnSelectAll(self):
        self.log.debug('%s itmes is selected', self.GetSelectedItemCount())
        if self.GetSelectedItemCount():
            for i in range(self.GetItemCount()):
                if self.IsSelected(i):
                    self.Select(i)

    def refresh(self):
        self.pop(self.path)

    def GetAllSelected(self):
        items = []
        for i in range(self.GetItemCount()):
            if self.IsSelected(i):
                items.append(i)
        return items

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

    def GetColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        self.log.debug(
            "Selected: %s, %s, %s, %s" % (
                self.currentItem,
                self.GetItemText(self.currentItem),
                self.GetColumnText(self.currentItem, 1),
                self.GetColumnText(self.currentItem, 2)
            )
        )

        event.Skip()

    def OnDoubleClick(self, event):
        self.log.debug('double clicked')
        try:
            text = self.GetItemText(self.currentItem)
        except Exception, e:
            self.log.debug(e)
            return
        self.log.debug(self.path)
        self.log.debug(text)
        fullname = os.path.join(self.path, text)
        self.log.debug("fullfilename:%s", fullname)
        if os.access(fullname, os.R_OK):
            if os.path.isdir(fullname):
                self.path = fullname
                self.log.debug('getting in path: %s', fullname)
                self.pop(self.path)
            else:
                self.open_file(fullname)
        else:
            self.mainWin.sb.SetStatusText('Permission denied')
        event.Skip()

    def OnLeftDown(self, event):
        self.log.debug('OnLeftDown')
        self.mainWin.activeListId = self.GetId()
        self.mainWin.sb.SetStatusText(self.path)
        event.Skip()

    def open_file(self, filename):
        self.log.debug("open file: %s", filename)


class FileMouse(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.log = logging.getLogger("MainWindow")

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        self.sb = self.CreateStatusBar()

        self.activeListId = ID_LEFTLIST
        leftList = FileListCtrl(self.splitter, ID_LEFTLIST)
        rightList = FileListCtrl(self.splitter, ID_RIGHTLIST)
        path1 = '/tmp'
        path2 = '/tmp'
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

        button1 = wx.Button(self, ID_BUTTON_VIEW, "F3 View")
        button2 = wx.Button(self, ID_BUTTON + 2, "F4 Edit")
        button3 = wx.Button(self, ID_BUTTON_COPY, "F5 Copy")
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
        self.Bind(wx.EVT_BUTTON, self.OnView, id=ID_BUTTON_VIEW)
        self.Bind(wx.EVT_BUTTON, self.OnCopy, id=ID_BUTTON_COPY)

        self.Bind(wx.EVT_LEFT_UP, self.OnClick)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        # 最大化
        # size = wx.DisplaySize()
        # self.SetSize(size)
        self.SetSize((800, 600))

        self.Center()
        self.Show(True)

    def OnClick(self, event):
        self.log.debug("clicked")
        event.Skip()

    def OnCopy(self, event):
        self.log.debug("On Copy Button pressed")
        self.log.debug("active win:%s", self.activeListId)
        if self.activeListId == ID_LEFTLIST:
            sourceList = self.FindWindowById(ID_LEFTLIST)
            targetList = self.FindWindowById(ID_RIGHTLIST)
        else:
            targetList = self.FindWindowById(ID_LEFTLIST)
            sourceList = self.FindWindowById(ID_RIGHTLIST)
        fileIndexs = sourceList.GetAllSelected()
        for index in fileIndexs:
            filename = sourceList.GetItemText(index)
            self.log.debug("copy %s to %s", filename, targetList.path)
            fullname = os.path.join(sourceList.path, filename)
            targetDir = targetList.path

            if os.access(fullname, os.R_OK) and os.access( targetDir, os.W_OK):
                if os.path.isfile(fullname):
                    shutil.copy2(fullname, targetDir)
                if os.path.isdir(fullname):
                    shutil.copytree(
                        fullname, os.path.join(targetDir, filename))
            else:
                dlg = wx.MessageDialog(
                    self,
                    'Copy %s to\n %s'% (fullname, targetList.path),
                    'Access Permission denied',
                    wx.OK | wx.ICON_INFORMATION
                    #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                )
                dlg.ShowModal()
                dlg.Destroy()

        targetList.refresh()

        event.Skip()

    def OnView(self, event):
        self.log.debug("On View Button pressed")
        self.log.debug("active win:%s", self.activeListId)
        list = self.FindWindowById(self.activeListId)
        print list.GetId()
        print list.GetAllSelected()
        event.Skip()

    def OnExit(self, event):
        self.Close(True)
        event.Skip()

    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        self.sb.SetStatusText(os.getcwd())
        event.Skip()

    def OnDoubleClick(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        event.Skip()


app = wx.App(0)
FileMouse(None, -1, 'File Mouse')
app.MainLoop()
