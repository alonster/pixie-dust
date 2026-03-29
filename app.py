from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from hex_view import HexView


class PixieDust(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield HexView(file_path='demo.bin')
        yield Footer()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
