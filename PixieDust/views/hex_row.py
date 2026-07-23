from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text

from PixieDust.utils.enums import ActiveSection
from PixieDust.utils.schema import Field
from PixieDust.utils.styles import Color


class HexRow(Static):
    selected_column = reactive(-1)
    active_section = reactive(ActiveSection.NONE)
    active_field: reactive[Field | None] = reactive(None)

    def __init__(self, offset: int, data: memoryview):
        super().__init__()
        self.data_offset = offset
        self.data = data

    @staticmethod
    def byte_color(byte: int) -> str:
        if byte == 0x00:
            return Color.white
        elif byte == 0xff:
            return Color.bright_red
        elif 0 < byte < 32 or byte == 0x7f:
            return Color.bright_green
        elif 32 <= byte <= 126:
            return Color.cyan

        return Color.dark_orange

    def add_selected_style(self, style: str, is_active: bool) -> str:
        if self.active_section.is_editable() and is_active:
            return f"bold {Color.black} on {style} blink"
        return f"{style} on {Color.bright_black} bold"

    @staticmethod
    def byte_representation(byte: int, current_section: ActiveSection) -> str:
        if current_section == ActiveSection.Hex:
            return f"{byte:02x}"

        if byte == 0x00 or byte == 0xff:
            return "⋄"
        elif 0 < byte < 32 or byte == 0x7f:
            return "•"
        elif 32 <= byte <= 126:
            return chr(byte)

        return "×"

    def render_section(self, current_section: ActiveSection) -> Text:
        section_text = Text()
        is_active = (self.active_section == current_section)
        field = self.active_field

        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            data_repr = self.byte_representation(byte, current_section)
            absolute_pos = self.data_offset + position
            is_field_highlight = (field is not None and field.offset <= absolute_pos < field.offset + field.size)

            if position == self.selected_column:
                style = self.add_selected_style(style, is_active)
            elif is_field_highlight:
                style = f"{style} on #36294c"

            section_text.append(data_repr, style=style)
            if current_section == ActiveSection.Hex:
                section_text.append(" ")

            if position == 7:
                section_text.append("┊", style=Color.white)
                if current_section == ActiveSection.Hex:
                    section_text.append(" ")

        padding_needed = 16 - len(self.data)
        for padding in range(padding_needed):
            section_text.append("   " if current_section == ActiveSection.Hex else " ")
            if padding_needed - padding == 9:
                section_text.append("┊", style=Color.white)
                if current_section == ActiveSection.Hex:
                    section_text.append(" ")

        return section_text

    def render_hex_section(self, line: Text):
        line.append(self.render_section(ActiveSection.Hex))

    def render_ascii_section(self, line: Text):
        line.append(self.render_section(ActiveSection.ASCII))

    def render(self) -> Text:
        line = Text()

        # Offset
        line.append("[", style=Color.white)
        line.append(f"{self.data_offset:08x}", style=Color.bright_black)
        line.append("] ", style=Color.white)

        self.render_hex_section(line)
        line.append("│ ", style=Color.white)
        self.render_ascii_section(line)
        return line
