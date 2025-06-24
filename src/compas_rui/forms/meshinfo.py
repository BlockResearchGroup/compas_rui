import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore

from compas.datastructures import Mesh


class MeshInfoForm(Eto.Forms.Dialog[bool]):
    """Form for working with mesh data.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    title : str, optional
        Title of the dialog.
    width : int, optional
        Window width.
    height : int, optional
        Window height.
    vertex_attr_names : list[str]
        The names of vertex attributes to include.
    edge_attr_names : list[str]
        The names of edge attributes to include
    face_attr_names : list[str]
        The names of face attributes to include.

    """

    def __init__(
        self,
        mesh: Mesh,
        vertex_attr_names,
        edge_attr_names,
        face_attr_names,
        title="Mesh Data",
        width=800,
        height=800,
    ):
        super().__init__()

        self.mesh = mesh
        self.vertex_attr_names = vertex_attr_names
        self.edge_attr_names = edge_attr_names
        self.face_attr_names = face_attr_names

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.vertexpage = Page(
            title="Vertices",
            keys=list(self.mesh.vertices()),
            names=self.vertex_attr_names,
            valuefunc=self.mesh.vertex_attribute,
            defaults=self.mesh.default_vertex_attributes,
        )
        self.edgepage = Page(
            title="Edges",
            keys=list(self.mesh.edges()),
            names=self.edge_attr_names,
            valuefunc=self.mesh.edge_attribute,
            defaults=self.mesh.default_edge_attributes,
        )
        self.facepage = Page(
            title="Faces",
            keys=list(self.mesh.faces()),
            names=self.face_attr_names,
            valuefunc=self.mesh.face_attribute,
            defaults=self.mesh.default_face_attributes,
        )
        control = Eto.Forms.TabControl()
        control.TabPosition = Eto.Forms.DockPosition.Top
        control.Pages.Add(self.vertexpage.widget)
        control.Pages.Add(self.edgepage.widget)
        control.Pages.Add(self.facepage.widget)

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(0, 12, 0, 12), Eto.Drawing.Size(0, 0), True, True)
        layout.AddRow(control)
        layout.EndVertical()
        layout.BeginVertical(Eto.Drawing.Padding(12, 18, 12, 24), Eto.Drawing.Size(6, 0), False, False)
        layout.AddRow(None, self.ok, self.cancel)
        layout.EndVertical()
        self.Content = layout

    @property
    def ok(self):
        self.DefaultButton = Eto.Forms.Button()
        self.DefaultButton.Text = "OK"
        self.DefaultButton.Click += self.on_ok
        return self.DefaultButton

    @property
    def cancel(self):
        self.AbortButton = Eto.Forms.Button()
        self.AbortButton.Text = "Cancel"
        self.AbortButton.Click += self.on_cancel
        return self.AbortButton

    def on_ok(self, sender, event):
        """Callback for the OK event."""
        self.Close(True)

    def on_cancel(self, sender, event):
        """Callback for the CANCEL event."""
        self.Close(False)

    def show(self):
        """Show the form dialog."""
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


class Page:
    """Wrapper for Eto tab pages.

    Parameters
    ----------
    title : str
        The title of the tab page.
    defaults : dict[str, Any]
        Default values of the data attributes.
    keys : list[int | tuple[int, int]]
        The identifiers of the mesh components.
    valuefunc : callable
        Function for retrieving the value of a named data attribute of a specific component.

    Attributes
    ----------
    names : list[str]
        The names of the attributes, in alphabetical order.
    public : list[str]
        The names of the editable attributes.
    private : list[str]
        The names of the read-only attributes.
    cols : list[dict]
        A list of dicts with each dict representing the properties of a data column.
    rows : list[list[str]]
        The data per mesh components corresponding to the columns.

    """

    def __init__(self, title, keys, names, valuefunc, defaults):
        self.defaults = defaults
        self.keys = keys
        self.names = names
        self.valuefunc = valuefunc
        self.table = Table(self.cols, self.rows)
        self.widget = Eto.Forms.TabPage()
        self.widget.Text = title
        if self.names:
            # replace this by a dynamic layout
            # with the first row an overview of the default attribute values
            # and second row the data table
            self.widget.Content = self.table.widget

    @property
    def cols(self):
        cols = [{"name": "ID", "precision": None}]
        for name in self.names:
            default = self.defaults[name]
            col = {"name": name, "precision": None}
            if isinstance(default, float):
                col["precision"] = "3f"
            cols.append(col)
        return cols

    @property
    def rows(self):
        rows = []
        for key in self.keys:
            row = [str(key)]
            for col in self.cols[1:]:
                name = col["name"]
                precision = col["precision"]
                value = self.valuefunc(key, name)
                if precision:
                    value = "{0:.{1}}".format(float(value), precision)
                else:
                    value = str(value)
                row.append(value)
            rows.append(row)
        return rows


class Table(object):
    """Wrapper for Eto grid view.

    Parameters
    ----------
    cols
    rows

    """

    def __init__(self, cols, rows):
        # def on_cell_formatting(sender, e):
        #     try:
        #         if not e.Column.Editable:
        #             e.ForegroundColor = Eto.Drawing.Colors.DarkGray
        #     except Exception as e:
        #         print(e)

        self.widget = Eto.Forms.GridView()
        self.widget.ShowHeader = True

        for i, col in enumerate(cols):
            column = Eto.Forms.GridColumn()
            column.HeaderText = col["name"]
            column.Editable = False
            cell = Eto.Forms.TextBoxCell(i)
            cell.VerticalAlignment = Eto.Forms.VerticalAlignment.Center
            cell.TextAlignment = Eto.Forms.TextAlignment.Right
            column.DataCell = cell
            self.widget.Columns.Add(column)

        collection = []
        for row in rows:
            item = Eto.Forms.GridItem()
            values = tuple(str(val) if val is not None else "" for val in row)
            item.Values = values
            collection.append(item)

        self.widget.DataStore = collection

        # self.widget.CellFormatting += on_cell_formatting

        self.cols = cols
        self.rows = rows
        self.data = self.widget.DataStore
