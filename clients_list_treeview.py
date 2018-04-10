import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import db_operations


work_record = db_operations.retrieve_user_work_record()

class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Client List TreeView Filter")
        self.set_default_size(400, 300)
        print(self.get_size())
        self.set_border_width(10)

        # setting up the grid in which elements will go
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.work_record_liststore = \
            Gtk.ListStore(str, str, str, float)
        for record in work_record:
            self.work_record_liststore.append(list(record))
        self.current_filter_client = None

        # Creating Filter, feeding it with the liststore model
        self.client_filter = self.work_record_liststore.filter_new()
        # setting the filter function
        self.client_filter.set_visible_func(self.client_filter_func)

        # creating the TreeView, making it use the
        # filter as a model and adding columns
        self.treeview = Gtk.TreeView.new_with_model(self.client_filter)
        self.treeview_selection = self.treeview.get_selection()
        self.treeview_selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.columns = ["Client Name", "Project", "Date", "Hours"]
        for i, column_title in enumerate(self.columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        # combo box to filter records by client
        self.cbo_client = Gtk.ComboBoxText()
        self.cbo_client.append_text("All Clients")
        self.cbo_client.set_active(0)
        self.btn_export = Gtk.Button("Export TimeSheet")
        self.btn_export.connect("clicked", self.export_timesheet, self.client_filter)

        clients_list = self.get_clients()
        for client in clients_list:
            self.cbo_client.append_text(client[0])
        self.cbo_client.connect("changed", self.on_combo_selection_changed)

        # setting up layout, TreeView goes into a window and combo box text
        #  goes below it
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 3, 12)
        self.grid.attach_next_to(self.cbo_client, self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.btn_export, self.cbo_client, Gtk.PositionType.RIGHT,1,1)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()
        self.get_clients()

    def client_filter_func(self, model, iter, data):
        """Tests if the client in the row is the one in the filter"""
        if self.current_filter_client is None or \
                        self.current_filter_client == "All Clients":
            return True
        else:
            return model[iter][0] == self.current_filter_client


    def on_combo_selection_changed(self, widget):
        self.current_filter_client = widget.get_active_text()
        self.client_filter.refilter()

    def get_clients(self):
        return db_operations.retrieve_client_list()

    def export_timesheet(self, widget, data):
        # This function allows the user to select the work records they want
        # to export to the spreadsheet or database.
        rows_to_export = []
        model, selected_rows = self.treeview_selection.get_selected_rows()
        if selected_rows != None:
            for row in selected_rows:
                print(model[row][0:])
                rows_to_export.append(model[row][0:])

        return rows_to_export



win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all
Gtk.main()
