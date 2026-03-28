from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Label

from hex_grid import HexGrid


class Inspector(Vertical):
    """Side panel for data interpretation."""

    def compose(self) -> ComposeResult:
        yield Label("--- INSPECTOR ---", id="inspector-title")
        yield Label("Value (Int8): --", id="val-int8")
        yield Label("Value (Hex): --", id="val-hex")
        yield Label("Value (Char): --", id="val-ascii")


class PixieDust(App):
    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            yield HexGrid(id="hex-grid")
            yield Inspector(id="inspector-panel")
        yield Footer()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
