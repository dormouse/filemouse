#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'

import os
import time
from gi.repository import Gtk, Gdk, GdkPixbuf
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s')

class MyTreeView(Gtk.TreeView):
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.log = logging.getLogger('MyTreeView')
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def pop(self, path):
        # get top window
        length = self.get_path().length()
        #print self.get_parent().get_parent().get_parent().get_parent().get_parent()
        print self.get_path().length()
        print self.get_path().to_string()


        self.path = path
        self.names = [u'图像', u'文件名', u'扩展名', u'大小', u'修改时间']
        self.types = [str, str, str, int, str]
        self.init_datas()
        pix_cel = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn('', pix_cel, stock_id=0)
        self.append_column(column)

        """
        Keep for make icon and filename together
        Always show warning when test, so keep for later.
        ---------------------------------------------------

        filename_col = Gtk.TreeViewColumn(names[1])
        pix_cel = Gtk.CellRendererPixbuf()
        str_cel = Gtk.CellRendererText()
        filename_col.pack_start(pix_cel, False)
        filename_col.pack_start(str_cel, False)
        filename_col.set_cell_data_func(pix_cel, self.get_tree_cell_pixbuf)
        filename_col.set_cell_data_func(str_cel, self.get_tree_cell_text)
        self.append_column(filename_col)
        """

        for i, column_title in enumerate(self.names[1:]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i + 1)
            self.append_column(column)

        select = self.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

        self.connect("button-press-event", self.on_button_press_event)

    def goto_up_path(self):
        """ 转到上一级目录 """
        if self.path != '/':
            self.path = os.path.split(self.path)[0]
            self.init_datas()

    def init_datas(self):
        infos = self.get_infos()
        self.model = Gtk.ListStore(*self.types)
        self.set_model(self.model)
        for info in infos:
            self.model.append(info)

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.log.debug("You selected %s", model[treeiter][1])
            self.current_filename = model[treeiter][1].decode('utf-8')

    def on_button_press_event(self, widget, event):
        self.log.debug("clicked")
        self.log.debug(type(widget))
        self.log.debug("eve type: %s", event.type)
        # Check if right mouse button was preseed
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            # self.log.debug(self.parent())
            length = self.get_path().length()
            print self.get_parent().get_parent().get_parent().get_parent().get_parent()
            print self.get_path().length()
            print self.get_path().to_string()
            parent = self.get_parent()
            for i in range(length-2):
                print parent
                parent = parent.get_parent()
            print parent
            parent.popup.popup(None, None, None, None, event.button, event.time)
            return True   # event has been handled
        if event.type ==Gdk.EventType._2BUTTON_PRESS:
            self.on_double_clicked()
            return True   # event has been handled

    def on_double_clicked(self):
        self.log.debug('double clicked')
        self.log.debug(self.current_filename)
        self.log.debug(type(self.current_filename))
        full_filename = os.path.join(self.path, self.current_filename)
        if os.path.isdir(full_filename):
            self.path = full_filename
            self.init_datas()
            self.log.debug('get in path: %s', full_filename)
        else:
            self.open_file(full_filename)

    def open_file(self, filename):
        self.log.debug("open file: %s", filename)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        """
        Keep for make icon and filename together
        Always show warning when test, so keep for later.
        """
        cell.set_property('text', self.model.get_value(iter, 1))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        """
        Keep for make icon and filename together
        Always show warning when test, so keep for later.
        """
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
            pic = Gtk.STOCK_DIRECTORY
            ext_name = '<dir>'
        else:
            pic = Gtk.STOCK_FILE
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
