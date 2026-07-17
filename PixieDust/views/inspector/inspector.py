from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import TabbedContent, TabPane

from PixieDust.utils.data_manager import DataManager
from PixieDust.views.inspector.mini import MiniInspector
from PixieDust.views.inspector.raw import RawInspector
from PixieDust.views.inspector.schema_view import SchemaView
from PixieDust.views.inspector.base_inspector import BaseInspectorView
from PixieDust.utils.styles import Color


class Inspector(Vertical):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        self.mini = MiniInspector()
        self.tabs = TabbedContent()
        self.raw_view = RawInspector(self.data_manager)
        self.schema_view = SchemaView(self.data_manager)

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

    def on_focus(self) -> None:
        self.raw_view.refresh_highlight(is_focused=True)
        self.schema_view.refresh_highlight(is_focused=True)

    def on_blur(self) -> None:
        self.raw_view.refresh_highlight(is_focused=False)
        self.schema_view.refresh_highlight(is_focused=False)

    def on_key(self, event: events.Key) -> None:
        if self.tabs.active == "raw":
            self.raw_view.handle_key_event(event)
        elif self.tabs.active == "schema":
            self.schema_view.handle_key_event(event)

    def on_base_inspector_view_edit_ended(self, event: BaseInspectorView.EditEnded) -> None:
        self.focus()

    def update_info(self, update: DataManager.PositionUpdate) -> None:
        full_data = self.data_manager.get_data()
        self.raw_view.update_info(update)
        active_field = self.schema_view.update_info(full_data, update.position)
        self.mini.update_field(active_field)
