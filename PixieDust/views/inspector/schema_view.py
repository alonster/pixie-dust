from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Label

from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.schema import Schema, Field
from PixieDust.views.inspector.grid import KeyValueGrid
from PixieDust.views.inspector.editable_field import EditableField
from PixieDust.views.inspector.base_inspector import BaseInspectorView
from PixieDust.utils.styles import Color


class SchemaView(BaseInspectorView):
    def __init__(self, data_manager: DataManager, schema: Schema | None = None):
        super().__init__(data_manager)
        # Placeholder demo schema
        self.schema = schema or Schema("Demo Schema", [
            Field("Magic", "uint32"),
            Field("Version", "uint16"),
            Field("Flags", "uint8"),
            Field("Negative", "int8"),
            Field("Offset", "uint32"),
            Field("Size", "uint32"),
        ])
        self.title = Label(f" {self.schema.name}")
        self.grid = None
        self.active_index = 0

    def compose(self) -> ComposeResult:
        yield self.title
        with VerticalScroll():
            with KeyValueGrid() as grid:
                self.grid = grid
                for field in self.schema.fields:
                    widget = EditableField("-")
                    self.field_widgets.append((field, widget))
                    yield from grid.add_pair(field.name, widget)

    def on_mount(self) -> None:
        self._apply_title_style()

    def _apply_title_style(self) -> None:
        self.title.styles.background = Color.mediumpurple
        self.title.styles.color = Color.white
        self.title.styles.text_style = "bold"
        self.title.styles.padding = (0, 1)
        self.title.styles.margin = (0, 0, 1, 0)

    def update_info(self, data: memoryview, current_position: int) -> Field:
        active_field = Field("Raw Byte", "uint8", offset=current_position, value=data[current_position])
        if not self.schema:
            return active_field

        self.schema.parse(data)
        self.active_index = -1

        for index, field in enumerate(self.schema.fields):
            _, widget = self.field_widgets[index]
            is_active = field.offset <= current_position < field.offset + field.size
            if is_active:
                active_field = field
                self.active_index = index

            widget.update_value(field.format())

        if not self.is_focused_view:
            self.selected_index = self.active_index

        self._apply_widget_styles()
        return active_field
