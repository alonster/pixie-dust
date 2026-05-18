from textual.app import ComposeResult
from textual.containers import Vertical, Grid, VerticalScroll
from textual.widgets import Label, Static

from PixieDust.schema.schema import Schema, Field
from PixieDust.styles import Color


class SchemaView(Vertical):
    def __init__(self, schema: Schema = None):
        super().__init__()
        # Placeholder demo schema
        self.schema = schema or Schema("Demo Schema", [
            Field("Magic", "uint32"),
            Field("Version", "uint16"),
            Field("Flags", "uint16"),
            Field("Data Offset", "uint32"),
            Field("Size", "uint32"),
        ])
        self.title = Label(f" {self.schema.name}")
        self.field_widgets = []

    def compose(self) -> ComposeResult:
        yield self.title
        with VerticalScroll():
            with Grid(id="fields-grid") as grid:
                self.grid = grid
                for field in self.schema.fields:
                    label = Label(f"{field.name}:")
                    value_static = Static("-")
                    self.field_widgets.append(value_static)
                    yield label
                    yield value_static

    def on_mount(self) -> None:
        self._apply_styles()

    def _apply_styles(self) -> None:
        self.title.styles.background = Color.mediumpurple
        self.title.styles.color = Color.white
        self.title.styles.text_style = "bold"
        self.title.styles.padding = (0, 1)
        self.title.styles.margin = (0, 0, 1, 0)

        self.grid.styles.padding = (0, 1)
        self.grid.styles.grid_size_columns = 2
        self.grid.styles.grid_columns = "1fr 1fr"
        self.grid.styles.grid_gutter_vertical = 1
        self.grid.styles.grid_gutter_horizontal = 1
        self.grid.styles.height = "auto"

        for child in self.grid.children:
            if isinstance(child, Label):
                child.styles.color = Color.orange
                child.styles.content_align = ("right", "middle")
            elif isinstance(child, Static):
                child.styles.background = Color.deep_grey
                child.styles.color = Color.white
                child.styles.border_left = ("solid", Color.mediumpurple)
                child.styles.padding = (0, 1)

    def update_info(self, data: memoryview, current_position: int) -> Field:
        active_field = Field("Raw Byte", "uint8", offset=current_position, value=data[current_position])
        if not self.schema:
            return active_field

        self.schema.parse(data)

        for field, widget in zip(self.schema.fields, self.field_widgets):
            is_active = field.offset <= current_position < field.offset + field.size
            if is_active:
                active_field = field

            # Update value text
            if field.value is None:
                val_str = "??"
            elif isinstance(field.value, int):
                val_str = f"{field.value} (0x{field.value:X})"
            elif isinstance(field.value, float):
                val_str = f"{field.value:.4f}"
            else:
                val_str = str(field.value)

            widget.update(val_str)

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
