from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label
from rich.text import Text


class HexRow(Static):
    """A widget displaying a single row of hex data."""

    def __init__(self, offset: int, data: bytes):
        super().__init__()
        self.data_offset = offset
        self.data = data

    def render(self) -> Text:
        line = Text()

        # Offset
        line.append(f"{self.data_offset:08x}")
        line.append(" │ ", style="white")

        # Hex View with color coding
        for position, byte in enumerate(self.data):
            if byte == 0x00:
                style = "bright_black"
            elif byte == 0xff:
                style = "bright_red"
            elif 32 <= byte <= 126:
                style = "cyan"
            else:
                style = "white"  # Others

            line.append(f"{byte:02x} ", style=style)

            # Put space between 8-byte blocks
            if position == 7:
                line.append("┊ ", style="white")

        line.append(" │ ", style="white")

        # ASCII View
        for position, byte in enumerate(self.data):
            if 32 <= byte <= 126:
                line.append(chr(byte), style="cyan")
            else:
                line.append("•", style="bright_black")

            # Put space between 8-byte blocks
            if position == 7:
                line.append("┊", style="white")

        return line


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
            with Vertical(id="hex-area"):
                # Initial dummy data for visual testing
                for i in range(0, 512, 16):
                    yield HexRow(i, b"\x00\x41\x42\x43\xff\x00\x20\x21" * 2)
            yield Inspector(id="inspector-panel")
        yield Footer()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
