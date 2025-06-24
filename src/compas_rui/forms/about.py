from typing import Optional

import Eto.Forms  # type: ignore
import Rhino.UI  # type: ignore
import System  # type: ignore


class AboutForm:
    def __init__(
        self,
        title: str,
        description: str,
        version: str,
        website: str,
        copyright: str,
        license: str,
        designers: Optional[list[str]] = None,
        developers: Optional[list[str]] = None,
        documenters: Optional[list[str]] = None,
    ) -> None:
        designers = designers or []
        developers = developers or []
        documenters = documenters or []

        self.dialog = Eto.Forms.AboutDialog()
        self.dialog.Copyright = copyright
        self.dialog.Designers = System.Array[System.String](designers)
        self.dialog.Developers = System.Array[System.String](developers)
        self.dialog.Documenters = System.Array[System.String](documenters)
        self.dialog.License = license
        self.dialog.ProgramDescription = description
        self.dialog.ProgramName = title
        self.dialog.Title = title
        self.dialog.Version = version
        self.dialog.Website = System.Uri(website)

    def show(self):
        self.dialog.ShowDialog(Rhino.UI.RhinoEtoApp.MainWindow)
