import struct

from textual.app import ComposeResult
from textual.containers import Vertical, Grid
from textual.widgets import Label, Static

from PixieDust.data_manager import DataManager


class Inspector(Vertical):
    address_value = Static()
    byte_value = Static()
    bin_value = Static()
    u32_le = Static()
    u32_be = Static()

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager

    def compose(self) -> ComposeResult:
        yield Label("Data Inspector", id="inspector-title")

        with Grid(id="inspector-grid"):
            yield Label("Address:", classes="table-label")
            self.address_value = Static("0x00000000", classes="table-value")
            yield self.address_value

            yield Label("Byte/U8:", classes="table-label")
            self.byte_value = Static("0x00 | 0", classes="table-value")
            yield self.byte_value

            yield Label("Binary:", classes="table-label")
            self.bin_value = Static("00000000", classes="table-value")
            yield self.bin_value

            yield Label("UInt32 LE:", classes="table-label")
            self.u32_le = Static("-", classes="table-value")
            yield self.u32_le

            yield Label("UInt32 BE:", classes="table-label")
            self.u32_be = Static("-", classes="table-value")
            yield self.u32_be

    def on_mount(self) -> None:
        self.styles.background = "#161616"
        self.set_styles("border-left: tall #7d5fff; padding: 1;")

        title = self.query_one("#inspector-title")
        title.styles.text_style = "bold"
        title.styles.content_align = ("center", "middle")
        title.styles.width = "100%"
        title.styles.background = "#212121"

        grid = self.query_one("#inspector-grid")
        grid.styles.padding = (1, 0)
        grid.styles.grid_size_columns = 2
        grid.styles.grid_columns = "10 1fr"
        grid.styles.grid_gutter_vertical = 1
        grid.styles.grid_gutter_horizontal = 1
        grid.styles.height = "auto"

        for label in self.query(".table-label"):
            label.styles.color = "darkorange"
            label.styles.text_style = "bold"
            label.styles.content_align = ("right", "middle")

        for val in self.query(".table-value"):
            val.styles.background = "#1e272e"
            val.styles.color = "whitesmoke"
            val.styles.padding = (0, 1)

        self.can_focus = True

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
