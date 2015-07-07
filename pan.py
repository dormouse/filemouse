#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'dormouse'


from gi.repository import Gtk, Gdk, GdkPixbuf
from treeview import MyTreeView
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)s %(funcName)s %(levelname)s %(message)s')

class MyPan(Gtk.Box):

    def __init__(self, path):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.log = logging.getLogger('MyPan')
        self.path = path

        toolbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.entry_path = Gtk.Entry()
        self.entry_path.set_text(self.path)
        self.btn_up_path = Gtk.Button(label="..")
        toolbox.pack_start(self.entry_path, True, True, 0)
        toolbox.pack_end(self.btn_up_path, False, False, 0)

        self.tree = MyTreeView()
        self.tree.pop(self.path)

        self.sw = Gtk.ScrolledWindow()
        self.sw.add(self.tree)

        self.pack_start(toolbox, False, False, 0)
        self.pack_start(self.sw, True, True, 0)

        self.btn_up_path.connect("clicked", self.on_but_up_path_clicked)

    def on_but_up_path_clicked(self, button):
        self.log.debug("but_up_path_clicked")
        self.tree.goto_up_path()
        self.entry_path.set_text(self.tree.path)

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        path = u'/home/dormouse/视频'
        pan = MyPan(path)
        self.set_default_size(200, 200)
        self.add(pan)


if __name__ == '__main__':
    win = MyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()