from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label


class HexRow(Static):
    """A widget displaying a single row of hex data."""

    def __init__(self, offset: int, data: bytes):
        super().__init__()
        self.data_offset = offset
        self.data = data

    def render(self) -> str:
        # Formatting: Offset | Hex Bytes | ASCII
        hex_part = " ".join(f"{b:02x}" for b in self.data)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in self.data)
        return f"[yellow]{self.data_offset:08x}[/yellow] | {hex_part:<47} | [green]{ascii_part}[/green]"


class Inspector(Vertical):
    """Side panel for data interpretation."""

    def compose(self) -> ComposeResult:
        yield Label("--- INSPECTOR ---", id="inspector-title")
        yield Label("Value (Int8): --", id="val-int8")
        yield Label("Value (Hex): --", id="val-hex")
        yield Label("Value (Char): --", id="val-ascii")


class PixieDust(App):
    CSS = """
    Screen {
        layers: base;
    }

    #main-container {
        height: 100%;
    }

    #hex-area {
        width: 75%;
        border: solid $accent;
        padding: 1;
        overflow-y: scroll;
    }

    #inspector-panel {
        width: 25%;
        border-left: tall $primary;
        background: $surface;
        padding: 1;
    }

    #inspector-title {
        text-style: bold;
        margin-bottom: 1;
        color: $secondary;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="hex-area"):
                # Initial dummy data for visual testing
                for i in range(0, 256, 16):
                    yield HexRow(i, b"\x00" * 16)
            yield Inspector(id="inspector-panel")
        yield Footer()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
