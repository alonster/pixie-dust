import struct

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from PixieDust.utils.data_manager import DataManager
from PixieDust.views.inspector.grid import KeyValueGrid

class RawInspector(Vertical):
    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

        self.address_value = Static("0x00000000")
        self.byte_value = Static("0x00 | 0")
        self.bin_value = Static("00000000")
        self.u32_le = Static("-")
        self.u32_be = Static("-")

    def compose(self) -> ComposeResult:
        with KeyValueGrid() as grid:
            yield from grid.add_pair("Address", self.address_value)
            yield from grid.add_pair("Byte/U8", self.byte_value)
            yield from grid.add_pair("Binary", self.bin_value)
            yield from grid.add_pair("UInt32 LE", self.u32_le)
            yield from grid.add_pair("UInt32 BE", self.u32_be)

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
