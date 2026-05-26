from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from PixieDust.views.hex_view import HexView
from PixieDust.views.quit_screen import UnsavedQuitScreen, EditingQuitScreen


class PixieDust(App):
    BINDINGS = [
        ("q", "quit_with_check", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
        ("ctrl+s", "save", "Save"),
    ]

    def __init__(self):
        super().__init__()
        self.hex_view = HexView()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.hex_view
        yield Footer()

    def action_toggle_edit(self) -> None:
        self.hex_view.action_toggle_edit()

    def action_save(self) -> None:
        self.hex_view.save_file()

    def action_quit_with_check(self) -> None:
        if self.hex_view.has_unsaved_changes:
            self.push_screen(UnsavedQuitScreen(), self.check_quit_callback)
        elif self.hex_view.active_section.is_editable():
            self.push_screen(EditingQuitScreen(), self.check_quit_callback)
        else:
            self.exit()

    def check_quit_callback(self, quit_confirmed: bool | None) -> None:
        if quit_confirmed:
            self.exit()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
