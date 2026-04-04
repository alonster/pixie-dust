from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from PixieDust.hex_view import HexView
from PixieDust.quit_screen import QuitScreen


class PixieDust(App):
    BINDINGS = [
        ("q", "quit_with_check", "Quit"),
        ("o", "open_file", "Open"),
        ("e", "toggle_edit", "Edit Mode"),
        ("ctrl+s", "save", "Save"),
    ]

    hex_view = HexView('')

    def compose(self) -> ComposeResult:
        yield Header()
        self.hex_view = HexView(file_path='demo.bin')
        yield self.hex_view
        yield Footer()

    def action_toggle_edit(self) -> None:
        self.hex_view.action_toggle_edit()

    def action_save(self) -> None:
        self.hex_view.save_file()

    def action_quit_with_check(self) -> None:
        message = ""
        if self.hex_view.has_unsaved_changes:
            message = "⚠️  UNSAVED CHANGES!\nYou'll lose your work. Are you sure you want to quit?"
        elif self.hex_view.active_section.is_editable():
            message = "📝 STILL EDITING!\nYou are in Edit Mode. Are you sure you want to quit?"

        if message:
            self.push_screen(QuitScreen(message), self.check_quit_callback)
        else:
            self.exit()

    def check_quit_callback(self, quit_confirmed: bool) -> None:
        if quit_confirmed:
            self.exit()


if __name__ == "__main__":
    app = PixieDust()
    app.run()
