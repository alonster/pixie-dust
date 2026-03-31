from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive

from PixieDust.hex_row import HexRow


class HexGrid(Vertical):
    _current_pos = reactive(0)
    is_editing = reactive(False)
    _edit_buffer = ""

    BINDINGS = [
        Binding("up", "move_up", show=False),
        Binding("down", "move_down", show=False),
        Binding("left", "move_left", show=False),
        Binding("right", "move_right", show=False),
        Binding("escape", "exit_edit_mode", show=False),
    ]

    def __init__(self, data: memoryview):
        super().__init__()
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
        self.watch(self.parent, "is_editing", self._sync_edit_mode)

        self.styles.height = "100%"
        self.styles.padding = (1, 1)

        self.can_focus = True
        self.focus()
        self.refresh_selection()

    def watch__current_pos(self, new_pos: int) -> None:
        self.refresh_selection()
        self.post_message(self.PositionChanged(new_pos))

    def _sync_edit_mode(self, new_value: bool) -> None:
        self.is_editing = new_value
        self._edit_buffer = ""
        self.refresh_selection()

    def refresh_selection(self) -> None:
        rows = self.query(HexRow)
        for index, row in enumerate(rows):
            is_active_row = (index == self.current_row)
            row.selected_column = self.current_col if is_active_row else -1
            row.is_editing = self.is_editing if is_active_row else False

    def change_current_pos_by(self, relative_offset: int) -> None:
        self.current_pos += relative_offset
        self._edit_buffer = ""

    def action_move_up(self) -> None:
        self.change_current_pos_by(-16)

    def action_move_down(self) -> None:
        self.change_current_pos_by(16)

    def action_move_left(self) -> None:
        self.change_current_pos_by(-1)

    def action_move_right(self) -> None:
        self.change_current_pos_by(1)

    def action_exit_edit_mode(self) -> None:
        self.parent.is_editing = False
        self._edit_buffer = ""

    def on_key(self, event: "events.Key") -> None:
        if not self.is_editing:
            return

        character = event.character
        if character and character.lower() in "0123456789abcdef":
            event.stop()
            self.handle_hex_input(character.lower())
            return

    def handle_hex_input(self, hex_char: str) -> None:
        full_hex = self._edit_buffer + hex_char
        new_byte_value = int(full_hex, 16)
        self.update_byte(new_byte_value)

        if not self._edit_buffer:
            self._edit_buffer = hex_char
        else:
            self._edit_buffer = ""
            self.current_pos += 1
            self.refresh_selection()

    def update_byte(self, new_value: int):
        self.data[self.current_pos] = new_value
        self.parent.has_unsaved_changes = True

        rows = self.query(HexRow)
        if self.current_row < len(rows):
            rows[self.current_row].refresh()

    def compose(self) -> ComposeResult:
        for offset in range(0, len(self.data), 16):
            yield HexRow(offset, self.data[offset:offset + 16])
