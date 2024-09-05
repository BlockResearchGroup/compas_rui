import Eto.Forms  # type: ignore
import Rhino.UI  # type: ignore
import System  # type: ignore


class AboutForm:
    def __init__(
        self,
        title,  # type: str
        description,  # type: str
        version,  # type: str
        website,  # type: str
        copyright,  # type: str
        license,  # type: str
        designers=None,  # type: list[str] | None
        developers=None,  # type: list[str] | None
        documenters=None,  # type: list[str] | None
    ):
        # type: (...) -> None
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
