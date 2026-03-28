from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static
from rich.text import Text


class HexRow(Static):
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


class HexGrid(Vertical):
    def compose(self) -> ComposeResult:
        with open('demo.bin', 'rb') as demo_file:
            demo_data = demo_file.read()

        with Vertical(id="hex-grid-vertical"):
            for offset in range(0, len(demo_data), 16):
                yield HexRow(offset, demo_data[offset:offset + 16])
