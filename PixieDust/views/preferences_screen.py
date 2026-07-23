from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Switch

from PixieDust.utils.preferences_manager import PreferencesManager
from PixieDust.utils.styles import Color


class PreferencesScreen(ModalScreen[None]):
    def compose(self) -> ComposeResult:
        with Vertical(id="container"):
            yield Label("Preferences", id="title")

            for opt in PreferencesManager.OPTIONS:
                with Horizontal(classes="setting_row"):
                    yield Label(opt.label, classes="setting_label")
                    yield Switch(value=PreferencesManager[opt.key], id=opt.key)

            with Horizontal(id="button_row"):
                yield Button("Close", variant="primary", id="close")

    def on_mount(self) -> None:
        self.styles.align = ("center", "middle")
        self.styles.background = "#000000 60%"

        container = self.query_one("#container")
        container.styles.width = 70
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

        for row in self.query(".setting_row"):
            row.styles.height = 3
            row.styles.align = ("left", "middle")
            row.styles.margin = (0, 0, 1, 0)
            row.styles.padding = (0, 1)
            row.styles.background = Color.deep_grey
            label = row.query_one(".setting_label")
            label.styles.width = "75%"
            label.styles.height = "100%"
            label.styles.content_align = ("left", "middle")

        btn_row = self.query_one("#button_row")
        btn_row.styles.width = "100%"
        btn_row.styles.height = 3
        btn_row.styles.align = ("center", "middle")
        btn_row.styles.margin = (1, 0, 0, 0)

        btn = self.query_one("#close")
        btn.styles.width = 20
        btn.focus()

    def on_switch_changed(self, event: Switch.Changed) -> None:
        if event.switch.id:
            key = str(event.switch.id)
            PreferencesManager.set(key, event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close":
            self.dismiss()

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            event.stop()
            self.dismiss()
