from textual import events
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.reactive import reactive

from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.enums import ActiveSection
from PixieDust.views.hex_row import HexRow


class HexGrid(Vertical):
    active_section = reactive(ActiveSection.NONE)
    _edit_buffer = ""

    BINDINGS = [
        Binding("up", "move_up", show=False),
        Binding("down", "move_down", show=False),
        Binding("left", "move_left", show=False),
        Binding("right", "move_right", show=False),
        Binding("escape", "exit_edit_mode", show=False),
    ]

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

    def on_mount(self) -> None:
        dom_parent = self.parent
        if dom_parent is not None:
            self.watch(dom_parent, "active_section", self._apply_active_section)

        self.styles.height = "100%"
        self.styles.padding = (1, 1)

        self.can_focus = True
        self.focus()
        self.refresh_selection()

    def _apply_active_section(self, new_value: ActiveSection) -> None:
        self.active_section = new_value
        self.refresh_selection()

    def refresh_selection(self) -> None:
        self._edit_buffer = ""
        rows = self.query(HexRow)
        for index, row in enumerate(rows):
            is_active_row = (index == self.data_manager.current_row)
            row.selected_column = self.data_manager.current_col if is_active_row else -1
            row.active_section = self.active_section if is_active_row else ActiveSection.NONE
            row.active_field = self.data_manager.active_field

    def action_move_up(self) -> None:
        self.data_manager.move_up()

    def action_move_down(self) -> None:
        self.data_manager.move_down()

    def action_move_left(self) -> None:
        self.data_manager.move_left()

    def action_move_right(self) -> None:
        self.data_manager.move_right()

    def action_exit_edit_mode(self) -> None:
        if self.parent is not None:
            setattr(self.parent, "active_section", ActiveSection.NONE)

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
            self.data_manager.update_byte_and_advance(ord(char))

    def handle_hex_input(self, hex_char: str) -> None:
        full_hex = self._edit_buffer + hex_char
        new_byte_value = int(full_hex, 16)

        if not self._edit_buffer:
            self.data_manager.update_byte(new_byte_value)
            self._edit_buffer = hex_char
        else:
            self._edit_buffer = ""
            self.data_manager.update_byte_and_advance(new_byte_value)

    def update_data(self, data_update: DataManager.DataUpdate):
        rows = self.query(HexRow)
        if data_update.length == 1:
            rows[self.data_manager.get_row_for_position(data_update.position)].refresh()
        else:
            min_row = self.data_manager.get_row_for_position(data_update.position)
            max_row = self.data_manager.get_row_for_position(data_update.position + data_update.length)
            for row_number in range(min_row, max_row + 1):
                rows[row_number].refresh()

    def compose(self) -> ComposeResult:
        for offset in range(0, len(self.data_manager.get_data()), 16):
            yield HexRow(offset, self.data_manager.get_data()[offset:offset + 16])
