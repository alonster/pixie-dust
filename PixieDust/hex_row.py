from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text


class HexRow(Static):
    selected_column = reactive(-1)
    is_editing = reactive(False)

    def __init__(self, offset: int, data: memoryview):
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

    def add_selected_style(self, style: str) -> str:
        if self.is_editing:
            return f"bold black on {style} blink"
        return style + " reverse bold"

    @staticmethod
    def byte_representation(byte: int, is_raw=False) -> str:
        if is_raw:
            return f"{byte:02x}"

        if byte == 0x00 or byte == 0xff:
            return "⋄"
        elif 0 < byte < 32 or byte == 0x7f:
            return "•"
        elif 32 <= byte <= 126:
            return chr(byte)

        return "×"

    def render_section(self, is_hex=False) -> Text:
        section = Text()
        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            data_repr = self.byte_representation(byte, is_raw=is_hex)
            if position == self.selected_column:
                style = self.add_selected_style(style)

            section.append(data_repr, style=style)
            if is_hex:
                section.append(" ")

            if position == 7:
                section.append("┊", style="white")
                if is_hex:
                    section.append(" ")

        return section

    def render_hex_section(self, line: Text):
        line.append(self.render_section(is_hex=True))

    def render_ascii_section(self, line: Text):
        line.append(self.render_section(is_hex=False))

    def render(self) -> Text:
        line = Text()

        # Offset
        line.append("│", style="white")
        line.append(f"{self.data_offset:08x}", style="bright_black")
        line.append("│ ", style="white")

        self.render_hex_section(line)
        line.append("│ ", style="white")
        self.render_ascii_section(line)
        return line
