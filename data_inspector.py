import struct

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label, Static


class Inspector(Vertical):
    def compose(self) -> ComposeResult:
        yield Label("Data Inspector", id="inspector-title")

        yield Label("Byte | UInt8:", classes="label-sub")
        yield Static("0x00 | 0", id="inspect-byte", classes="value-display")

        yield Label("Binary:", classes="label-sub")
        yield Static("00000000", id="inspect-bin", classes="value-display")

        yield Label("UInt32 (Little / Big Endian):", classes="label-sub")
        yield Static("0 / 0", id="inspect-uint32", classes="value-display")

        yield Label("Address:", classes="label-sub")
        yield Static("0x00000000", id="inspect-address", classes="value-display")

    def update_info(self, pos: int, data_chunk: bytes) -> None:
        if len(data_chunk) >= 1:
            byte = data_chunk[0]
            self.query_one("#inspect-byte", Static).update(f"0x{byte:02x} | {byte}")
            self.query_one("#inspect-bin", Static).update(f"{byte:08b}")

        val_u32_l = "-"
        val_u32_b = "-"
        if len(data_chunk) >= 4:
            val_u32_l = struct.unpack("<I", data_chunk[:4])[0]
            val_u32_b = struct.unpack(">I", data_chunk[:4])[0]

        self.query_one("#inspect-uint32", Static).update(f"{val_u32_l} / {val_u32_b}")
        self.query_one("#inspect-address", Static).update(f"0x{pos:08X}")
