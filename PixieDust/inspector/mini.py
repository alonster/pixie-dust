from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label

from PixieDust.styles import Color


class MiniInspector(Vertical):
    def __init__(self):
        super().__init__()
        self.label_name = Label("Field: -")
        self.label_offset = Label("Address:  0x00000000")
        self.label_value = Label("Value: -")

    def compose(self) -> ComposeResult:
        yield self.label_name
        yield self.label_offset
        yield self.label_value

    def on_mount(self) -> None:
        self.styles.height = 6
        self.styles.padding = (1, 1)
        self.styles.background = Color.dark_grey
        self.styles.border_bottom = ("solid", Color.black)

        self.label_name.styles.text_style = "bold"
        self.label_name.styles.color = Color.orange

        self.label_offset.styles.color = Color.grey

        self.label_value.styles.text_style = "bold"
        self.label_value.styles.color = Color.white

    def update_field(self, name: str, value: str, offset: int):
        self.label_name.update(f"Field: {name}")
        self.label_offset.update(f"Address:  0x{offset:08X}")
        self.label_value.update(f"Value: {value}")
