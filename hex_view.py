from textual.app import ComposeResult
from textual.containers import Horizontal

from hex_grid import HexGrid
from data_inspector import Inspector


class HexView(Horizontal):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.data = b''
        self.grid = HexGrid(b'')
        self.inspector = Inspector()

    def compose(self) -> ComposeResult:
        with open(self.file_path, 'rb') as f:
            self.data = f.read()

        self.grid = HexGrid(self.data)
        self.inspector = Inspector()

        yield self.grid
        yield self.inspector

    def on_mount(self) -> None:
        self.styles.height = "100%"
        self.styles.width = "100%"
        self.grid.styles.width = "70%"
        self.inspector.styles.width = "30%"

    def on_hex_grid_position_changed(self, message: "HexGrid.PositionChanged") -> None:
        data_chunk = self.data[message.pos: message.pos + 4]
        self.inspector.update_info(message.pos, data_chunk)
