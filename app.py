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

    @staticmethod
    def byte_color(byte: int) -> str:
        if byte == 0x00:
            return "bright_black"
        elif byte == 0xff:
            return "bright_red"
        elif 0 < byte < 32 or byte == 0x7f:
            return "bright_green"
        elif 32 <= byte <= 126:
            return "cyan"

        return "dark_orange"

    @staticmethod
    def byte_representation(byte: int) -> str:
        if byte == 0x00 or byte == 0xff:
            return "⋄"
        elif 0 < byte < 32 or byte == 0x7f:
            return "•"
        elif 32 <= byte <= 126:
            return chr(byte)

        return "×"

    def render(self) -> Text:
        line = Text()

        # Offset
        line.append("│", style="white")
        line.append(f"{self.data_offset:08x}", style="bright_black")
        line.append("│ ", style="white")

        # Hex View with color coding
        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            line.append(f"{byte:02x} ", style=style)

            # Put space between 8-byte blocks
            if position == 7:
                line.append("┊ ", style="white")

        line.append("│ ", style="white")

        # ASCII View
        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            byte_repr = self.byte_representation(byte)
            line.append(byte_repr, style=style)

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
                with open('demo.bin', 'rb') as demo_file:
                    demo_data = demo_file.read()
                    for offset in range(0, len(demo_data), 16):
                        yield HexRow(offset, demo_data[offset:offset+16])
            yield Inspector(id="inspector-panel")
        yield Footer()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
