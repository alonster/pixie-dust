from enum import Enum
from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text


class Section(Enum):
    Hex = "Hex"
    ASCII = "ASCII"


class HexRow(Static):
    selected_column = reactive(-1)
    active_section = reactive(Section.Hex)
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

    def add_selected_style(self, style: str, is_active: bool) -> str:
        if self.is_editing and is_active:
            return f"bold black on {style} blink"
        return style + " on bright_black bold"

    @staticmethod
    def byte_representation(byte: int, current_section: Section) -> str:
        if current_section == Section.Hex:
            return f"{byte:02x}"

        if byte == 0x00 or byte == 0xff:
            return "⋄"
        elif 0 < byte < 32 or byte == 0x7f:
            return "•"
        elif 32 <= byte <= 126:
            return chr(byte)

        return "×"

    def render_section(self, current_section: Section) -> Text:
        section_text = Text()
        is_active = (self.active_section == current_section)

        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            data_repr = self.byte_representation(byte, current_section)
            if position == self.selected_column:
                style = self.add_selected_style(style, is_active)

            section_text.append(data_repr, style=style)
            if current_section == Section.Hex:
                section_text.append(" ")

            if position == 7:
                section_text.append("┊", style="white")
                if current_section == Section.Hex:
                    section_text.append(" ")

        padding_needed = 16 - len(self.data)
        for padding in range(padding_needed):
            section_text.append("   " if current_section == Section.Hex else " ")
            if padding_needed - padding == 9:
                section_text.append("┊", style="white")
                if current_section == Section.Hex:
                    section_text.append(" ")

        return section_text

    def render_hex_section(self, line: Text):
        line.append(self.render_section(Section.Hex))

    def render_ascii_section(self, line: Text):
        line.append(self.render_section(Section.ASCII))

    def render(self) -> Text:
        line = Text()

        # Offset
        line.append("[", style="white")
        line.append(f"{self.data_offset:08x}", style="bright_black")
        line.append("] ", style="white")

        self.render_hex_section(line)
        line.append("│ ", style="white")
        self.render_ascii_section(line)
        return line
