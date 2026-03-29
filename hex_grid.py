from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static
from rich.text import Text


class HexRow(Static):
    selected_column = reactive(-1)

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
    def add_selected_style(style: str) -> str:
        return style + " reverse bold"

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

        # Hex View
        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            if position == self.selected_column:
                style = self.add_selected_style(style)

            line.append(f"{byte:02x}", style=style)
            line.append(" ")

            # Put space between 8-byte blocks
            if position == 7:
                line.append("┊ ", style="white")

        line.append("│ ", style="white")

        # ASCII View
        for position, byte in enumerate(self.data):
            style = self.byte_color(byte)
            byte_repr = self.byte_representation(byte)
            if position == self.selected_column:
                style = self.add_selected_style(style)

            line.append(byte_repr, style=style)

            # Put space between 8-byte blocks
            if position == 7:
                line.append("┊", style="white")

        return line


class HexGrid(Vertical):
    _current_pos = reactive(0)

    BINDINGS = [
        Binding("up", "move_up", show=False),
        Binding("down", "move_down", show=False),
        Binding("left", "move_left", show=False),
        Binding("right", "move_right", show=False),
    ]

    def __init__(self, data: bytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    class PositionChanged(Message):
        def __init__(self, pos: int):
            self.pos = pos
            super().__init__()

    @property
    def current_pos(self) -> int:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: int) -> None:
        max_pos = max(0, (len(self.data)) - 1)
        self._current_pos = max(0, min(value, max_pos))

    @property
    def current_row(self) -> int:
        return self.current_pos // 16

    @property
    def current_col(self) -> int:
        return self.current_pos % 16

    def on_mount(self) -> None:
        self.styles.height = "100%"
        self.styles.padding = (1, 1)

        self.can_focus = True
        self.focus()
        self.refresh_selection()

    def watch__current_pos(self, new_pos: int) -> None:
        self.refresh_selection()
        self.post_message(self.PositionChanged(new_pos))

    def refresh_selection(self) -> None:
        rows = self.query(HexRow)
        for index, row in enumerate(rows):
            row.selected_column = self.current_col if index == self.current_row else -1

    def action_move_up(self) -> None:
        self.current_pos -= 16

    def action_move_down(self) -> None:
        self.current_pos += 16

    def action_move_left(self) -> None:
        self.current_pos -= 1

    def action_move_right(self) -> None:
        self.current_pos += 1

    def compose(self) -> ComposeResult:
        for offset in range(0, len(self.data), 16):
            yield HexRow(offset, self.data[offset:offset + 16])
