from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive

from PixieDust.utils.file_manager import FileManager
from PixieDust.utils.schema import Field


class DataManager(Container):
    _current_pos = reactive(0)
    _active_field: reactive[Field | None] = reactive(None)
    _data = bytearray(b'')

    BYTES_IN_ROW = 16

    class PositionUpdate(Message):
        def __init__(self, position: int):
            super().__init__()
            self.position = position

    class DataUpdate(PositionUpdate):
        def __init__(self, position: int, length: int):
            super().__init__(position)
            self.length = length

    def load_data_from_file(self):
        if not self._data:
            self._data = FileManager.read_data_from_file()
            self.current_pos = 0

    def save_data_to_file(self):
        FileManager.save_data_to_file(self._data)

    def get_data(self) -> memoryview:
        return memoryview(self._data)

    @property
    def current_pos(self) -> int:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: int) -> None:
        max_pos = max(0, (len(self._data)) - 1)
        self._current_pos = max(0, min(value, max_pos))

    @property
    def active_field(self) -> Field | None:
        return self._active_field

    @active_field.setter
    def active_field(self, value: Field | None) -> None:
        if self._active_field != value:
            self._active_field = value
            self.post_message(self.PositionUpdate(self.current_pos))

    @property
    def current_row(self) -> int:
        return self.get_row_for_position(self.current_pos)

    @property
    def current_col(self) -> int:
        return self.get_col_for_position(self.current_pos)

    def get_row_for_position(self, position: int) -> int:
        return position // self.BYTES_IN_ROW

    def get_col_for_position(self, position: int) -> int:
        return position % self.BYTES_IN_ROW

    def watch__current_pos(self, new_pos: int) -> None:
        self.post_message(self.PositionUpdate(new_pos))

    def change_current_pos_by(self, relative_offset: int) -> None:
        self.current_pos += relative_offset

    def move_up(self) -> None:
        self.change_current_pos_by(-16)

    def move_down(self) -> None:
        self.change_current_pos_by(16)

    def move_left(self) -> None:
        self.change_current_pos_by(-1)

    def move_right(self) -> None:
        self.change_current_pos_by(1)

    def update_byte(self, new_value: int):
        self._data[self.current_pos] = new_value
        self.post_message(self.DataUpdate(self.current_pos, length=1))

    def update_byte_and_advance(self, new_value: int):
        self.update_byte(new_value)
        self.current_pos += 1

    def update_data_range(self, offset: int, new_bytes: bytes):
        self._data[offset:offset + len(new_bytes)] = new_bytes
        self.post_message(self.DataUpdate(offset, length=len(new_bytes)))
