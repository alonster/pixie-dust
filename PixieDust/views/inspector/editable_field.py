from textual import events
from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static, Input
from PixieDust.utils.styles import Color


class InlineInput(Input):
    class CancelEdit(Message):
        def __init__(self, sender: "InlineInput") -> None:
            super().__init__()
            self.sender = sender

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            event.stop()
            self.post_message(self.CancelEdit(self))


class EditableField(Widget):
    is_editing = False

    def __init__(self, initial_value: str = "-"):
        super().__init__()
        self.static_val = Static(initial_value)
        self.input_val = InlineInput(value=initial_value)
        self.input_val.display = False

    def compose(self) -> ComposeResult:
        yield self.static_val
        yield self.input_val

    def on_mount(self) -> None:
        self.styles.height = "auto"
        
        self.static_val.styles.background = "transparent"
        self.static_val.styles.color = Color.white
        self.static_val.styles.padding = 0

        self.input_val.styles.height = 1
        self.input_val.styles.border = "none"
        self.input_val.styles.padding = (0, 1)
        self.input_val.styles.background = Color.deep_grey
        self.input_val.styles.color = Color.orange

    def update_value(self, new_value: str) -> None:
        self.static_val.update(new_value)
        if not self.is_editing:
            self.input_val.value = new_value

    def start_edit(self, edit_value: str) -> None:
        self.is_editing = True
        self.static_val.display = False
        self.input_val.display = True
        self.input_val.value = edit_value
        self.input_val.focus()

    def end_edit(self) -> None:
        self.is_editing = False
        self.static_val.display = True
        self.input_val.display = False
