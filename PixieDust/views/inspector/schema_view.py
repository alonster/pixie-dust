from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Label, Static

from PixieDust.utils.schema import Schema, Field
from PixieDust.views.inspector.grid import KeyValueGrid
from PixieDust.utils.styles import Color


class SchemaView(Vertical):
    def __init__(self, schema: Schema | None = None):
        super().__init__()
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
        self.field_widgets = []

    def compose(self) -> ComposeResult:
        yield self.title
        with VerticalScroll():
            with KeyValueGrid() as grid:
                self.grid = grid
                for field in self.schema.fields:
                    value_static = Static("-")
                    self.field_widgets.append(value_static)
                    yield from grid.add_pair(field.name, value_static)

    def on_mount(self) -> None:
        self._apply_styles()

    def _apply_styles(self) -> None:
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

        for field, widget in zip(self.schema.fields, self.field_widgets):
            is_active = field.offset <= current_position < field.offset + field.size
            if is_active:
                active_field = field

            widget.update(field.format())

            # Update highlighting
            if is_active:
                widget.styles.background = Color.mediumpurple
                widget.styles.color = Color.white
                widget.styles.text_style = "bold"
            else:
                widget.styles.background = Color.deep_grey
                widget.styles.color = Color.white
                widget.styles.text_style = "none"

        return active_field
