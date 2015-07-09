#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'

import wx
import os
import time

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


class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        files = os.listdir('.')

        self.fileType = FileType()
        self.il = wx.ImageList(16, 16)
        for pic in self.fileType.picFiles:
            print pic
            self.il.Add(wx.Bitmap(pic))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)


        j = 1
        self.InsertStringItem(0, '..')
        self.SetItemImage(0, 3)

        for i in files:
            (name, ext) = os.path.splitext(i)
            ex = ext[1:]
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)
            self.InsertStringItem(j, name)
            self.SetStringItem(j, 1, ex)
            self.SetStringItem(j, 2, str(size) + ' B')
            self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M',
                                                   time.localtime(sec)))

            if os.path.isdir(i):
                self.SetItemImage(j, self.fileType.GetIndex('dir'))
            elif ex == 'py':
                self.SetItemImage(j, self.fileType.GetIndex('python'))
            else:
                self.SetItemImage(j, self.fileType.GetIndex('unknown'))

            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')
            j = j + 1

    def GetFileInfos(self):
        files = os.listdir(self.path)
        infos = [self.GetFileInfo(filename) for file in files]
        return infos

    def GetFileInfo(self, filename):
        name = os.path.join(self.path, filename)
        mod_time = os.path.getmtime(name)
        mod_time = time.strftime(self.time_format,
                                 time.localtime(mod_time))
        size = os.path.getsize(name)
        if os.path.isdir(name):
            pic = Gtk.STOCK_DIRECTORY
            ext_name = '<dir>'
        else:
            pic = Gtk.STOCK_FILE
            ext_name = os.path.splitext(filename)[1][1:]

        return [pic, filename, ext_name, size, mod_time]


class FileMouse(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        p1 = MyListCtrl(self.splitter, -1)
        p2 = MyListCtrl(self.splitter, -1)
        self.splitter.SplitVertically(p1, p2)

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

        size = wx.DisplaySize()
        self.SetSize(size)

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
