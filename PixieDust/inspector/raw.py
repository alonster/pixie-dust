import struct

from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Label, Static

from PixieDust.data_manager import DataManager
from PixieDust.styles import Theme


class RawInspector(Vertical):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        self.address_value = Static("0x00000000")
        self.byte_value = Static("0x00 | 0")
        self.bin_value = Static("00000000")
        self.u32_le = Static("-")
        self.u32_be = Static("-")

        self.rows = {
            Label("Address:"): self.address_value,
            Label("Byte/U8:"): self.byte_value,
            Label("Binary:"): self.bin_value,
            Label("UInt32 LE:"): self.u32_le,
            Label("UInt32 BE:"): self.u32_be,
        }

    def compose(self) -> ComposeResult:
        with Grid() as grid:
            self.grid = grid
            for label, value in self.rows.items():
                yield label
                yield value

    def on_mount(self) -> None:
        self.grid.styles.padding = (1, 1)
        self.grid.styles.grid_size_columns = 2
        self.grid.styles.grid_columns = "10 1fr"
        self.grid.styles.grid_gutter_vertical = 1
        self.grid.styles.grid_gutter_horizontal = 1
        self.grid.styles.height = "auto"

        for label in self.rows.keys():
            label.styles.color = Theme.ACCENT_ORANGE
            label.styles.content_align = ("right", "middle")

        for val in self.rows.values():
            val.styles.background = Theme.BG_VALUE
            val.styles.color = Theme.TEXT_PRIMARY
            val.styles.border_left = ("solid", Theme.ACCENT_PURPLE)
            val.styles.padding = (0, 1)

    def update_info(self, update: DataManager.PositionUpdate) -> None:
        self.address_value.update(f"0x{update.position:08X}")
        data_chunk = self.data_manager.get_data()[update.position:update.position + 4]

        if len(data_chunk) >= 1:
            byte = data_chunk[0]
            self.byte_value.update(f"0x{byte:02X} | {byte}")
            self.bin_value.update(f"{byte:08b}")

        if len(data_chunk) >= 4:
            le = struct.unpack("<I", data_chunk[:4])[0]
            be = struct.unpack(">I", data_chunk[:4])[0]
            self.u32_le.update(str(le))
            self.u32_be.update(str(be))
        else:
            self.u32_le.update("-")
            self.u32_be.update("-")

        self.refresh()
