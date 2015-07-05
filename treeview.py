#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'

import os
import time
from gi.repository import Gtk, Gdk, GdkPixbuf

class MyTreeView(Gtk.TreeView):
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def pop(self, path):
        self.path = path
        names = [u'图像', u'文件名', u'扩展名', u'大小', u'修改时间']
        types = [str, str, str, int, str]
        infos = self.get_infos()

        self.model = Gtk.ListStore(*types)
        self.set_model(self.model)

        for info in infos:
            self.model.append(info)

        filename_col = Gtk.TreeViewColumn(names[1])
        pix_cel = Gtk.CellRendererPixbuf()
        str_cel = Gtk.CellRendererText()
        filename_col.pack_start(pix_cel, False)
        filename_col.pack_start(str_cel, False)
        filename_col.set_cell_data_func(pix_cel, self.get_tree_cell_pixbuf)
        filename_col.set_cell_data_func(str_cel, self.get_tree_cell_text)
        self.append_column(filename_col)


        for i, column_title in enumerate(names[2:]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i+2)
            self.append_column(column)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        cell.set_property('text', self.model.get_value(iter, 1))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file(self.model.get_value(iter, 0)))

    def get_infos(self):
        files = os.listdir(self.path)
        infos = [self.get_file_info(filename) for filename in files]
        return infos

    def get_file_info(self, filename):
        name = os.path.join(self.path, filename)
        mod_time = os.path.getmtime(name)
        mod_time = time.strftime(self.time_format,
                                 time.localtime(mod_time))
        size = os.path.getsize(name)
        if os.path.isdir(name):
            pic = 'folder.svg'
            ext_name = '<dir>'
        else:
            pic = 'python.png'
            ext_name = os.path.splitext(filename)[1][1:]

        return [pic, filename, ext_name, size, mod_time]

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)
        self.treeview = MyTreeView()
        path = u'/home/dormouse/视频'
        self.treeview.pop(path)
        self.add(self.treeview)


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()