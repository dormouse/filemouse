from gi.repository import Gtk
from gi.repository import GObject

class Person (GObject.GObject):
    name = GObject.property(type=str)
    age = GObject.property(type=int)
    gender = GObject.property(type=bool, default=True)

    def __init__(self):
        GObject.GObject.__init__(self)

    def __repr__(self):
        s = None
        if self.get_property("gender"): s = "m"
        else: s = "f"
        return "%s, %s, %i" % (self.get_property("name"), s, self.get_property("age"))

class MyApplication (Gtk.Window):

    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.set_title("Tree Display")
        self.set_size_request(400, 400)
        self.connect("destroy", Gtk.main_quit)
        self.create_widgets()
        self.insert_rows()
        self.show_all()

    def create_widgets(self):
        self.treestore = Gtk.TreeStore(Person.__gtype__)
        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.treestore)
        column = Gtk.TreeViewColumn("Person")

        cell = Gtk.CellRendererText()
        column.pack_start(cell, True)

        column.set_cell_data_func(cell, self.get_name)

        self.treeview.append_column(column)
        vbox = Gtk.VBox()
        self.add(vbox)
        vbox.pack_start(self.treeview, True, True, 0)

        button = Gtk.Button("Retrieve element")
        button.connect("clicked", self.retrieve_element)
        vbox.pack_start(button, False, False, 5)

    def get_name(self, column, cell, model, iter, data):
        cell.set_property('text', self.treestore.get_value(iter, 0).name)

    def insert_rows(self):
        for name, age, gender in [("Tom", 19, True), ("Anna", 35, False)]:
            p = Person()
            p.name = name
            p.age = age
            p.gender = gender
            self.treestore.append(None, (p,))

    def retrieve_element(self, widget):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter:
            print "You selected", model[treeiter][0]

if __name__ == "__main__":
    GObject.type_register(Person)
    MyApplication()
    Gtk.main()
