from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static


class HexViewer(Static):
    def on_mount(self) -> None:
        self.update("00000000: 48 65 6c 6c 6f 20 57 6f  72 6c 64 21 00 00 00 00  Hello World!....")


class PixieDust(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield HexViewer()
        yield Footer()

if __name__ == '__main__':
    app = PixieDust()
    app.run()
