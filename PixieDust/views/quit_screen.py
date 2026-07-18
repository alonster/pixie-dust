from textual import events
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label
from textual.containers import Horizontal, Vertical


class QuitScreen(ModalScreen[bool]):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="container"):
            yield Label(self.message, id="question")
            with Horizontal(id="buttons_row"):
                yield Button("Quit", variant="error", id="quit")
                yield Button("Cancel", variant="primary", id="cancel")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")

        container = self.query_one("#container")
        container.styles.width = 60
        container.styles.height = "auto"
        container.styles.border = ("tall", "gray")
        container.styles.padding = (1, 1)
        container.styles.align = ("center", "middle")

        question = self.query_one("#question")
        question.styles.text_align = "center"
        question.styles.width = "100%"
        question.styles.margin = (1, 0)
        question.styles.text_style = "bold"

        buttons_row = self.query_one("#buttons_row")
        buttons_row.styles.width = "100%"
        buttons_row.styles.height = 3
        buttons_row.styles.align = ("center", "middle")

        for btn_id in ["#quit", "#cancel"]:
            btn = self.query_one(btn_id)
            btn.styles.margin = (0, 8)
            btn.styles.width = 16

    def on_key(self, event: events.Key) -> None:
        if event.key in ("left", "right"):
            event.stop()
            self.focus_next()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)


class UnsavedQuitScreen(QuitScreen):
    def __init__(self):
        super().__init__("⚠️  UNSAVED CHANGES!\nYou'll lose your work. Are you sure you want to quit?")


class EditingQuitScreen(QuitScreen):
    def __init__(self):
        super().__init__("📝 STILL EDITING!\nYou are in Edit Mode. Are you sure you want to quit?")
