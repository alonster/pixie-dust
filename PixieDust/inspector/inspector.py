from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import TabbedContent, TabPane

from PixieDust.data_manager import DataManager
from PixieDust.inspector.mini import MiniInspector
from PixieDust.inspector.raw import RawInspector
from PixieDust.inspector.schema_view import SchemaView
from PixieDust.styles import Color


class Inspector(Vertical):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        self.mini = MiniInspector()
        self.tabs = TabbedContent()
        self.raw_view = RawInspector(self.data_manager)
        self.schema_view = SchemaView()

    def compose(self) -> ComposeResult:
        yield self.mini
        with self.tabs:
            with TabPane("Data Inspector", id="raw"):
                yield self.raw_view
            with TabPane("Schema View", id="schema"):
                yield self.schema_view

    def action_toggle_mode(self) -> None:
        self.tabs.active = "schema" if self.tabs.active == "raw" else "raw"

    def on_mount(self) -> None:
        self.styles.background = Color.dark_grey
        self.styles.border_left = ("tall", Color.mediumpurple)

        self.can_focus = True

    def update_info(self, update: DataManager.PositionUpdate) -> None:
        full_data = self.data_manager.get_data()
        self.raw_view.update_info(update)
        active_field = self.schema_view.update_info(full_data, update.position)
        self.mini.update_field(active_field.name, active_field.value, active_field.offset)
