from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from PixieDust.hex_view import HexView


class PixieDust(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
        ("ctrl+s", "save", "Save"),
    ]

    hex_view = HexView('')

    def compose(self) -> ComposeResult:
        yield Header()
        self.hex_view = HexView(file_path='demo.bin')
        yield self.hex_view
        yield Footer()

    def action_toggle_edit(self) -> None:
        self.hex_view.action_toggle_edit()

    def action_save(self) -> None:
        self.hex_view.save_file()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
