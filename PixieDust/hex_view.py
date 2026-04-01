import os

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive

from PixieDust.enums import ActiveSection
from PixieDust.hex_grid import HexGrid
from PixieDust.data_inspector import Inspector


class HexView(Horizontal):
    active_section = reactive(ActiveSection.NONE)
    has_unsaved_changes = reactive(False)

    BINDINGS = [
        ("tab", "next_section", "Next Section"),
    ]

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.data = bytearray()
        self.grid = HexGrid(memoryview(self.data))
        self.inspector = Inspector()

    @property
    def file_name(self):
        return os.path.basename(self.file_path)

    def compose(self) -> ComposeResult:
        with open(self.file_path, 'rb') as f:
            self.data = bytearray(f.read())

        self.grid = HexGrid(memoryview(self.data))
        self.inspector = Inspector()

        yield self.grid
        yield self.inspector

    def action_toggle_edit(self) -> None:
        if self.active_section == ActiveSection.NONE:
            self.active_section = ActiveSection.Hex
        else:
            self.active_section = ActiveSection.NONE

    def action_next_section(self) -> None:
        if self.active_section == ActiveSection.NONE:
            return

        if self.active_section == ActiveSection.Hex:
            self.active_section = ActiveSection.ASCII
        elif self.active_section == ActiveSection.ASCII:
            self.active_section = ActiveSection.Inspector
        elif self.active_section == ActiveSection.Inspector:
            self.active_section = ActiveSection.Hex
        self._update_focus()

    def _update_focus(self) -> None:
        if self.active_section == ActiveSection.Inspector:
            self.inspector.focus()
        else:
            self.grid.focus()
        self.grid.refresh_selection()

    def on_mount(self) -> None:
        self.styles.height = "100%"
        self.styles.width = "100%"
        self.grid.styles.width = "70%"
        self.inspector.styles.width = "30%"

        self._update_focus()
        self.update_title()

    def on_hex_grid_position_changed(self, message: "HexGrid.PositionChanged") -> None:
        data_chunk = self.data[message.pos: message.pos + 4]
        self.inspector.update_info(message.pos, data_chunk)

    def watch_has_unsaved_changes(self, value: bool) -> None:
        self.update_title()

    def update_title(self) -> None:
        indicator = " *" if self.has_unsaved_changes else ""
        self.app.title = f"PixieDust - {self.file_name}{indicator}"

    def save_file(self) -> None:
        try:
            with open(self.file_path, 'wb') as f:
                f.write(self.data)
            self.notify(f"Saved: {self.file_path}", severity="information")
            self.has_unsaved_changes = False
        except Exception as e:
            self.notify(f"Save failed: {e}", severity="error")
