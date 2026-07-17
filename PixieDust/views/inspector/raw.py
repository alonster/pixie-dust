from textual.app import ComposeResult
from textual.widgets import Static

from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.schema import Field
from PixieDust.views.inspector.grid import KeyValueGrid
from PixieDust.views.inspector.editable_field import EditableField
from PixieDust.views.inspector.base_inspector import BaseInspectorView
from PixieDust.utils.styles import Color

class RawInspector(BaseInspectorView):
    def __init__(self, data_manager: DataManager):
        super().__init__(data_manager)

        self.address_value = Static("0x00000000")
        self.fields = [
            Field("Byte/U8", "uint8"),
            Field("Binary", "binary"),
            Field("UInt32 LE", "uint32", is_little_endian=True),
            Field("UInt32 BE", "uint32", is_little_endian=False),
        ]

    def compose(self) -> ComposeResult:
        with KeyValueGrid() as grid:
            yield from grid.add_pair("Address", self.address_value)
            for field in self.fields:
                widget = EditableField("-")
                self.field_widgets.append((field, widget))
                yield from grid.add_pair(field.name, widget)

    def _apply_widget_styles(self) -> None:
        for index, (_, widget) in enumerate(self.field_widgets):
            if self.is_focused_view and index == self.selected_index:
                widget.styles.background = Color.mediumpurple
                widget.static_val.styles.text_style = "bold"
            else:
                widget.styles.background = Color.deep_grey
                widget.static_val.styles.text_style = "none"

    def update_info(self, update: DataManager.PositionUpdate) -> None:
        self.address_value.update(f"0x{update.position:08X}")
        data = self.data_manager.get_data()

        for field, widget in self.field_widgets:
            field.offset = update.position
            field.set_value(data)
            widget.update_value(field.format())

        self.refresh_highlight(self.is_focused_view)
        self.refresh()
