import os

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive

from PixieDust.enums import ActiveSection
from PixieDust.data_manager import DataManager
from PixieDust.hex_grid import HexGrid
from PixieDust.inspector.inspector import Inspector


class HexView(Horizontal):
    active_section = reactive(ActiveSection.NONE)
    has_unsaved_changes = reactive(False)

    BINDINGS = [
        ("tab", "next_section", "Next Section"),
        ("m", "toggle_mode", "Toggle Mode"),
    ]

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.data_manager = DataManager(bytearray(b''))
        self.grid = HexGrid(self.data_manager)
        self.inspector = Inspector(self.data_manager)

    @property
    def file_name(self):
        return os.path.basename(self.file_path)

    def compose(self) -> ComposeResult:
        with open(self.file_path, 'rb') as f:
            self.data_manager.set_data(bytearray(f.read()))

        yield self.data_manager
        yield self.grid
        yield self.inspector

    def action_toggle_edit(self) -> None:
        if self.active_section == ActiveSection.NONE:
            self.active_section = ActiveSection.Hex
        else:
            self.active_section = ActiveSection.NONE

    def action_toggle_mode(self) -> None:
        self.inspector.action_toggle_mode()

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

    def on_data_manager_position_update(self, message: DataManager.PositionUpdate) -> None:
        self.grid.refresh_selection()
        self.inspector.update_info(message)

    def on_data_manager_data_update(self, message: DataManager.DataUpdate) -> None:
        self.has_unsaved_changes = True
        self.grid.update_data(message)
        self.inspector.update_info(message)

    def watch_has_unsaved_changes(self, value: bool) -> None:
        self.update_title()

    def update_title(self) -> None:
        indicator = " *" if self.has_unsaved_changes else ""
        self.app.title = f"PixieDust - {self.file_name}{indicator}"

    def save_file(self) -> None:
        try:
            with open(self.file_path, 'wb') as f:
                f.write(self.data_manager.get_data())
            self.notify(f"Saved: {self.file_path}", severity="information")
            self.has_unsaved_changes = False
        except Exception as e:
            self.notify(f"Save failed: {e}", severity="error")
