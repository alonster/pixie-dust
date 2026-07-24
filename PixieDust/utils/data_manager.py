from pathlib import Path

from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive

from PixieDust.utils.schema import Field
from PixieDust.utils.enums import EditMode


class FileUtils:
    @staticmethod
    def read_data_from_file(path: Path) -> bytearray:
        with open(path, "rb") as f:
            return bytearray(f.read())

    @staticmethod
    def save_data_to_file(path: Path, data: bytearray) -> None:
        with open(path, "wb") as f:
            f.write(data)


class DataManager(Container):
    _current_pos = reactive(0)
    _active_field: reactive[Field | None] = reactive(None)
    _edit_mode = reactive(EditMode.INSERT)
    _data = bytearray()

    BYTES_IN_ROW = 16

    class PositionUpdate(Message):
        def __init__(self, position: int):
            super().__init__()
            self.position = position

    class DataUpdate(PositionUpdate):
        def __init__(self, position: int, length: int):
            super().__init__(position)
            self.length = length

    def __init__(self, file_path: Path | None = None, schema_path: Path | None = None):
        super().__init__()
        self.file_path = file_path
        self.schema_path = schema_path

    @property
    def file_name(self) -> str:
        return self.file_path.name if self.file_path else "Untitled"

    def load_data_from_file(self):
        if not self._data and self.file_path and self.file_path.exists() and self.file_path.is_file():
            self._data = FileUtils.read_data_from_file(self.file_path)
            self.current_pos = 0

    def save_data_to_file(self):
        if self.file_path:
            FileUtils.save_data_to_file(self.file_path, self._data)

    def get_data(self) -> memoryview:
        return memoryview(bytes(self._data))

    @property
    def current_pos(self) -> int:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: int) -> None:
        if self._edit_mode == EditMode.APPEND:
            max_pos = len(self._data)
        else:
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
    def edit_mode(self) -> EditMode:
        return self._edit_mode

    @edit_mode.setter
    def edit_mode(self, mode: EditMode) -> None:
        if self._edit_mode != mode:
            self._edit_mode = mode
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
        self.change_current_pos_by(-self.BYTES_IN_ROW)

    def move_down(self) -> None:
        self.change_current_pos_by(self.BYTES_IN_ROW)

    def move_left(self) -> None:
        self.change_current_pos_by(-1)

    def move_right(self) -> None:
        self.change_current_pos_by(1)

    def update_byte(self, new_value: int):
        if self._edit_mode == EditMode.INSERT:
            if self.current_pos < len(self._data):
                self._data[self.current_pos] = new_value
        elif self._edit_mode == EditMode.APPEND:
            if self.current_pos >= len(self._data):
                self._data.append(new_value)
            else:
                self._data.insert(self.current_pos, new_value)

        self.post_message(self.DataUpdate(self.current_pos, length=1))

    def update_byte_and_advance(self, new_value: int):
        if self.current_pos < len(self._data):
            self._data[self.current_pos] = new_value
            self.post_message(self.DataUpdate(self.current_pos, length=1))
        self.current_pos += 1

    def update_data_range(self, offset: int, new_bytes: bytes):
        self._data[offset:offset + len(new_bytes)] = new_bytes
        self.post_message(self.DataUpdate(offset, length=len(new_bytes)))

    def remove_byte(self, at_current: bool = True) -> None:
        target_pos = self.current_pos if at_current else self.current_pos - 1
        if target_pos < 0 or target_pos >= len(self._data):
            return

        if self._edit_mode == EditMode.INSERT:
            self._data[target_pos] = 0
        else:
            del self._data[target_pos]

        self.current_pos = target_pos
        self.post_message(self.DataUpdate(target_pos, length=1))
