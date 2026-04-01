from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive

from PixieDust.enums import ActiveSection
from PixieDust.hex_row import HexRow


class HexGrid(Vertical):
    _current_pos = reactive(0)
    active_section = reactive(ActiveSection.NONE)
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
        self.watch(self.parent, "active_section", self._apply_active_section)

        self.styles.height = "100%"
        self.styles.padding = (1, 1)

        self.can_focus = True
        self.focus()
        self.refresh_selection()

    def watch__current_pos(self, new_pos: int) -> None:
        self.refresh_selection()
        self.post_message(self.PositionChanged(new_pos))

    def _apply_active_section(self, new_value: ActiveSection) -> None:
        self.active_section = new_value
        self._edit_buffer = ""
        self.refresh_selection()

    def refresh_selection(self) -> None:
        rows = self.query(HexRow)
        for index, row in enumerate(rows):
            is_active_row = (index == self.current_row)
            row.selected_column = self.current_col if is_active_row else -1
            row.active_section = self.active_section if is_active_row else False

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
        self.parent.active_section = ActiveSection.NONE
        self._edit_buffer = ""

    def on_key(self, event: "events.Key") -> None:
        if not self.active_section.is_editable():
            return

        if self.active_section == ActiveSection.Hex:
            self._handle_hex_key(event)
        elif self.active_section == ActiveSection.ASCII:
            self._handle_ascii_key(event)

    def _handle_hex_key(self, event: "events.Key") -> None:
        character = event.character
        if character and character.lower() in "0123456789abcdef":
            event.stop()
            self.handle_hex_input(character.lower())

    def _handle_ascii_key(self, event: "events.Key") -> None:
        char = event.character
        if char and len(char) == 1 and char.isprintable():
            event.stop()
            self.update_byte_and_advance(ord(char))

    def handle_hex_input(self, hex_char: str) -> None:
        full_hex = self._edit_buffer + hex_char
        new_byte_value = int(full_hex, 16)

        if not self._edit_buffer:
            self.update_byte(new_byte_value)
            self._edit_buffer = hex_char
        else:
            self._edit_buffer = ""
            self.update_byte_and_advance(new_byte_value)

    def update_byte(self, new_value: int):
        self.data[self.current_pos] = new_value
        self.parent.has_unsaved_changes = True

        rows = self.query(HexRow)
        if self.current_row < len(rows):
            rows[self.current_row].refresh()

    def update_byte_and_advance(self, new_value: int):
        self.update_byte(new_value)
        self.current_pos += 1
        self.refresh_selection()

    def compose(self) -> ComposeResult:
        for offset in range(0, len(self.data), 16):
            yield HexRow(offset, self.data[offset:offset + 16])
