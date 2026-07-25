from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from PixieDust.utils.styles import Color


class GoToOffsetModal(ModalScreen[int | None]):
    def __init__(self, max_offset: int, current_offset: int = 0):
        super().__init__()
        self.max_offset = max_offset
        self.current_offset = current_offset

    def compose(self) -> ComposeResult:
        with Vertical(id="container"):
            yield Label("Go to Offset", id="title")
            yield Label(f"Enter hex (e.g. 0x10) or decimal (0..{self.max_offset}):", id="hint")
            yield Input(
                placeholder=f"Current: {hex(self.current_offset)} ({self.current_offset})",
                id="offset_input",
            )
            with Horizontal(id="button_row"):
                yield Button("Go", variant="primary", id="go")
                yield Button("Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self.styles.background = "#000000 60%"

        container = self.query_one("#container")
        container.styles.width = 60
        container.styles.height = "auto"
        container.styles.background = Color.dark_grey
        container.styles.border = ("tall", Color.mediumpurple)
        container.styles.padding = (1, 2)

        title = self.query_one("#title")
        title.styles.text_align = "center"
        title.styles.width = "100%"
        title.styles.margin = (0, 0, 1, 0)
        title.styles.text_style = "bold"
        title.styles.color = Color.mediumpurple

        hint = self.query_one("#hint")
        hint.styles.margin = (0, 0, 1, 0)

        inp = self.query_one("#offset_input", Input)
        inp.styles.margin = (0, 0, 1, 0)
        inp.focus()

        btn_row = self.query_one("#button_row")
        btn_row.styles.width = "100%"
        btn_row.styles.height = 3
        btn_row.styles.align = ("center", "middle")

        for btn_id in ["#go", "#cancel"]:
            btn = self.query_one(btn_id)
            btn.styles.margin = (0, 2)
            btn.styles.width = 14

    def parse_offset(self, value: str) -> int | None:
        value = value.strip()
        if value:
            try:
                offset = int(value, base=0)
                if 0 <= offset <= self.max_offset:
                    return offset
            except ValueError:
                pass

        return None
    
    def handle_input(self, value: str):
        offset = self.parse_offset(value)
        if offset is not None:
            self.dismiss(offset)
        else:
            self.notify(f"Invalid offset. Valid values are 0..{self.max_offset}.", severity="error")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        event.stop()
        self.handle_input(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go":
            offset_input = self.query_one("#offset_input", Input)
            self.handle_input(offset_input.value)
        else:
            self.dismiss(None)

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            event.stop()
            self.dismiss(None)
