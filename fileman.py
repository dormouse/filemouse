#!/usr/bin/python
# -*- coding: utf8 -*-

from gi.repository import Gtk, Gdk

from treeview import MyTreeView
from pan import MyPan, MyWindow

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
      <menu action='FileNew'>
        <menuitem action='FileNewStandard' />
        <menuitem action='FileNewFoo' />
        <menuitem action='FileNewGoo' />
      </menu>
      <separator />
      <menuitem action='FileQuit' />
    </menu>
    <menu action='EditMenu'>
      <menuitem action='EditCopy' />
      <menuitem action='EditPaste' />
      <menuitem action='EditSomething' />
    </menu>
    <menu action='ChoicesMenu'>
      <menuitem action='ChoiceOne'/>
      <menuitem action='ChoiceTwo'/>
      <separator />
      <menuitem action='ChoiceThree'/>
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='FileNewStandard' />
    <toolitem action='FileQuit' />
  </toolbar>
  <popup name='PopupMenu'>
    <menuitem action='EditCopy' />
    <menuitem action='EditPaste' />
    <menuitem action='EditSomething' />
  </popup>
</ui>
"""


class MenuExampleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="File Mouse")

        self.set_default_size(800, 400)

        # action
        action_group = Gtk.ActionGroup("my_actions")

        self.add_file_menu_actions(action_group)
        self.add_edit_menu_actions(action_group)
        self.add_choices_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")
        toolbar = uimanager.get_widget("/ToolBar")
        self.popup = uimanager.get_widget("/PopupMenu")

        # left tree view and right tree view
        test_path = u'/home/dormouse/视频'
        left_pan = MyPan(test_path)
        right_pan = MyPan(test_path)

        box_main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_main.pack_start(left_pan, True, True, 10)
        box_main.pack_start(right_pan, True, True, 10)

        btn_copy = Gtk.Button("Copy")
        btn_move = Gtk.Button("Move")
        btn_copy.connect("clicked", self.on_btn_copy_clicked)
        btn_move.connect("clicked", self.on_btn_move_clicked)
        box_opr = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_opr.pack_start(btn_copy, False, False, 0)
        box_opr.pack_start(btn_move, False, False, 0)

        box_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box_top.pack_start(menubar, False, False, 0)
        box_top.pack_start(toolbar, False, False, 0)
        box_top.pack_start(box_main, True, True, 0)
        box_top.pack_start(box_opr, False, False, 0)

        self.add(box_top)
        self.connect("button-press-event", self.on_button_press_event)

    def on_btn_copy_clicked(self, button):
        print("\"copy me\" button was clicked")

    def on_btn_move_clicked(self, button):
        print("\"move me\" button was clicked")

    def on_button_press_event(self, widget, event):
        print "clicked", widget, type(widget)
        # Check if right mouse button was preseed
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            self.popup.popup(None, None, None, None, event.button, event.time)
            return True   # event has been handled

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
        action_group.add_action(action_filenewmenu)

        action_new = Gtk.Action("FileNewStandard", "_New",
                                "Create a new file", Gtk.STOCK_NEW)
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action_with_accel(action_new, None)

        action_group.add_actions([
            ("FileNewFoo", None, "New Foo", None, "Create new foo",
             self.on_menu_file_new_generic),
            ("FileNewGoo", None, "_New Goo", None, "Create new goo",
             self.on_menu_file_new_generic),
        ])

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    def add_edit_menu_actions(self, action_group):
        action_group.add_actions([
            ("EditMenu", None, "Edit"),
            ("EditCopy", Gtk.STOCK_COPY, None, None, None,
             self.on_menu_others),
            ("EditPaste", Gtk.STOCK_PASTE, None, None, None,
             self.on_menu_others),
            ("EditSomething", None, "Something", "<control><alt>S", None,
             self.on_menu_others)
        ])

    def add_choices_menu_actions(self, action_group):
        action_group.add_action(Gtk.Action("ChoicesMenu", "Choices", None,
                                           None))

        action_group.add_radio_actions([
            ("ChoiceOne", None, "One", None, None, 1),
            ("ChoiceTwo", None, "Two", None, None, 2)
        ], 1, self.on_menu_choices_changed)

        three = Gtk.ToggleAction("ChoiceThree", "Three", None, None)
        three.connect("toggled", self.on_menu_choices_toggled)
        action_group.add_action(three)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(UI_INFO)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_file_new_generic(self, widget):
        print("A File|New menu item was selected.")

    def on_menu_file_quit(self, widget):
        Gtk.main_quit()

    def on_menu_others(self, widget):
        print("Menu item " + widget.get_name() + " was selected")

    def on_menu_choices_changed(self, widget, current):
        print(current.get_name() + " was selected.")

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            print(widget.get_name() + " activated")
        else:
            print(widget.get_name() + " deactivated")



window = MenuExampleWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
