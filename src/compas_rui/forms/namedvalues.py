import ast

import Eto.Drawing  # type: ignore
import Eto.Forms  # type: ignore
import Rhino  # type: ignore
import Rhino.UI  # type: ignore


class NamedValuesForm(Eto.Forms.Dialog[bool]):
    """Eto form for displaying and editing named values.

    Note that when providing a new value for a name-value pair,
    only literal Python structures are allowed: strings, bytes, numbers, tuples, lists, dicts, sets, booleans, and None
    Other types of values will be ignored.

    Parameters
    ----------
    names : list[str]
        The names of the values.
    values: list[str, byte, float, int, tuple, list, dict, set, bool, None]
        The values.
        Only literal Python structures are allowed.
        Other types of values are ignored.
    title : str, optional
        The title of the form window.
    width : int, optional
        The width of the form window.
    height : int, optional
        The height of the form window.

    """

    def __init__(
        self,
        names,  # type: list[str]
        values,  # type: list
        title="Named Values",  # type: str
        width=500,  # type: int
        height=500,  # type: int
    ):
        # type: (...) -> None

        super().__init__()

        def on_cell_formatting(sender, e):
            try:
                if not e.Column.Editable:
                    e.ForegroundColor = Eto.Drawing.Colors.DarkGray
            except Exception as e:
                print(e)

        self.attributes = dict(zip(names, values))
        self.names = names
        self.values = [str(value) for value in values]

        self.Title = title
        self.Padding = Eto.Drawing.Padding(0)
        self.Resizable = True
        self.MinimumSize = Eto.Drawing.Size(0.5 * width, 0.5 * height)
        self.ClientSize = Eto.Drawing.Size(width, height)

        self.table = table = Eto.Forms.GridView()
        table.ShowHeader = True

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Name"
        column.Editable = False
        column.Expand = True
        column.DataCell = Eto.Forms.TextBoxCell(0)
        table.Columns.Add(column)

        column = Eto.Forms.GridColumn()
        column.HeaderText = "Value"
        column.Editable = True
        column.DataCell = Eto.Forms.TextBoxCell(1)
        table.Columns.Add(column)

        collection = []
        for name, value in zip(self.names, self.values):
            item = Eto.Forms.GridItem()
            item.Values = (name, value)
            collection.append(item)
        table.DataStore = collection

        layout = Eto.Forms.DynamicLayout()
        layout.BeginVertical(Eto.Drawing.Padding(0, 0, 0, 0), Eto.Drawing.Size(0, 0), True, True)
        layout.AddRow(table)
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
        try:
            for row in self.table.DataStore:
                name = row.GetValue(0)
                value = row.GetValue(1)
                if value != "-":
                    try:
                        value = ast.literal_eval(value)
                    except Exception as e:
                        print(e)
                self.attributes[name] = value
        except Exception as e:
            print(e)
            self.Close(False)
        self.Close(True)

    def on_cancel(self, sender, event):
        self.Close(False)

    def show(self):
        return self.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)


if __name__ == "__main__":
    form = NamedValuesForm(names=["a", "b"], values=[1, 2])
    if form.show():
        print(form.attributes)
