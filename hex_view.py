from textual.app import ComposeResult
from textual.containers import Horizontal

from hex_grid import HexGrid
from data_inspector import Inspector


class HexView(Horizontal):
    """Main container that manages the data and coordinates between Grid and Inspector."""

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.data = b''

    def compose(self) -> ComposeResult:
        # Reading the data once here
        with open(self.file_path, 'rb') as f:
            self.data = f.read()

        # Pass the loaded data to the HexGrid
        yield HexGrid(self.data, id="hex-grid")
        yield Inspector(id="inspector-panel")

    def on_hex_grid_position_changed(self, message: "HexGrid.PositionChanged") -> None:
        """Update Inspector when the grid sends a PositionChanged message."""
        inspector = self.query_one(Inspector)

        data_chunk = self.data[message.pos: message.pos + 4]
        inspector.update_info(message.pos, data_chunk)
