from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive

from PixieDust.utils.enums import ActiveSection
from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.file_manager import FileManager
from PixieDust.views.hex_grid import HexGrid
from PixieDust.views.inspector.inspector import Inspector


class HexView(Horizontal):
    active_section = reactive(ActiveSection.NONE)
    has_unsaved_changes = reactive(False)

    BINDINGS = [
        ("tab", "next_section", "Next Section"),
        ("m", "toggle_mode", "Toggle Mode"),
    ]

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.grid = HexGrid(self.data_manager)
        self.inspector = Inspector(self.data_manager)

    def compose(self) -> ComposeResult:
        self.data_manager.load_data_from_file()

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
        self.grid.styles.width = 82
        self.inspector.styles.width = "100%"

        self._update_focus()
        self.update_title()

    def on_data_manager_position_update(self, message: DataManager.PositionUpdate) -> None:
        self.grid.refresh_selection()
        self.inspector.update_info(message)
        self.update_title(self.has_unsaved_changes)

    def on_data_manager_data_update(self, message: DataManager.DataUpdate) -> None:
        self.has_unsaved_changes = True
        self.grid.update_data(message)
        self.inspector.update_info(message)

    def watch_active_section(self, value: ActiveSection) -> None:
        self.update_title(self.has_unsaved_changes)

    def watch_has_unsaved_changes(self, value: bool) -> None:
        self.update_title(value)

    def update_title(self, has_unsaved_changes: bool = False) -> None:
        indicator = " *" if has_unsaved_changes else ""
        mode_badge = f" [{self.data_manager.edit_mode.value.upper()}]" if self.active_section.is_editable() else ""
        self.app.title = f"PixieDust - {FileManager.get_file_name()}{mode_badge}{indicator}"

    def save_file(self) -> None:
        try:
            self.data_manager.save_data_to_file()
            self.notify(f"Saved: {FileManager.get_file_name()}", severity="information")
            self.has_unsaved_changes = False
        except Exception as e:
            self.notify(f"Save failed: {e}", severity="error")
