from gi.repository import Gtk, GdkPixbuf
from gi.repository import GObject

class Person (GObject.GObject):
    name = GObject.property(type=str)
    age = GObject.property(type=int)
    gender = GObject.property(type=bool, default=True)
    pix = GObject.property(type=str)

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

        cell_text = Gtk.CellRendererText()
        column.pack_start(cell_text, True)

        cell_pix = Gtk.CellRendererPixbuf()
        column.pack_start(cell_pix, False)

        column.set_cell_data_func(cell_text, self.get_text)
        column.set_cell_data_func(cell_pix, self.get_pix)

        self.treeview.append_column(column)
        vbox = Gtk.VBox()
        self.add(vbox)
        vbox.pack_start(self.treeview, True, True, 0)

        button = Gtk.Button("Retrieve element")
        button.connect("clicked", self.retrieve_element)
        vbox.pack_start(button, False, False, 5)

    def get_text(self, column, cell, model, iter, data):
        cell.set_property('text', self.treestore.get_value(iter, 0).name)

    def get_pix(self, col, cell, model, iter, user_data):
        cell.set_property('pixbuf', GdkPixbuf.Pixbuf.new_from_file(model.get_value(iter, 0).pix))

    def insert_rows(self):
        for name, age, gender, pix in [("Tom", 19, True, "python.png"), ("Anna", 35, False, "python.png")]:
            p = Person()
            p.name = name
            p.age = age
            p.gender = gender
            p.pix = pix
            self.treestore.append(None, (p,))

    def retrieve_element(self, widget):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter:
            print "You selected", model[treeiter][0]

if __name__ == "__main__":
    GObject.type_register(Person)
    MyApplication()
    Gtk.main()
