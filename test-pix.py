#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'
from gi.repository import Gtk, Gdk, GdkPixbuf
from treeview import MyTreeView

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        self.treeview = MyTreeView()
        path = u'/home/dormouse/视频'
        self.treeview.pop(path)

        """
        self.liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.treeview = Gtk.TreeView(model=self.liststore)

        symbol1 = GdkPixbuf.Pixbuf.new_from_file("python.png")
        self.liststore.append([symbol1, "This is a symbol1"])

        symbol2 = Gtk.IconTheme.get_default().load_icon("gtk-cut", 64, 0)
        self.liststore.append([symbol2, "This is symbol2"])

        px_renderer = Gtk.CellRendererPixbuf()
        px_column = Gtk.TreeViewColumn("Icon", px_renderer, pixbuf=0)
        self.treeview.append_column(px_column)

        str_renderer = Gtk.CellRendererText()
        str_column = Gtk.TreeViewColumn("Name", str_renderer, text=1)
        self.treeview.append_column(str_column)
        """

        self.add(self.treeview)

        self.treeview.connect("button-press-event", self.on_button_press_event)

        select = self.treeview.get_selection()
        select.connect("changed", self.on_tree_selection_changed)

    def on_button_press_event(self,treeview,event):
        print "clicked"

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print "You selected", model[treeiter][1]

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()