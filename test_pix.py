#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'

from gi.repository import Gtk, Gdk, GdkPixbuf


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)

        self.liststore.append(["python.png", "This is a symbol1"])

        px_renderer = Gtk.CellRendererPixbuf()
        px_column = Gtk.TreeViewColumn('image')
        px_column.pack_start(px_renderer, False)
        str_renderer = Gtk.CellRendererText()
        px_column.pack_start(str_renderer, False)
        # set data connector function/method
        px_column.set_cell_data_func(px_renderer, self.get_tree_cell_pixbuf)
        px_column.set_cell_data_func(str_renderer, self.get_tree_cell_text)
        self.treeview.append_column(px_column)

        self.add(self.treeview)

    def get_tree_cell_text(self, col, cell, model, iter, user_data):
        cell.set_property('text', model.get_value(iter, 1))

    def get_tree_cell_pixbuf(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file(model.get_value(iter, 0)))

if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()