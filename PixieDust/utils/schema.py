import struct
from dataclasses import dataclass, field
from typing import List, Any


TYPE_MAP = {
    "uint8": "B",
    "uint16": "H",
    "uint32": "I",
    "uint64": "Q",
    "int8": "b",
    "int16": "h",
    "int32": "i",
    "int64": "q",
    "float": "f",
    "double": "d",
    "binary": "B",
}


@dataclass
class Field:
    name: str
    type: str
    is_little_endian: bool = True
    offset: int = 0
    value: Any = None

    @property
    def struct_format(self) -> str:
        code = TYPE_MAP.get(self.type.lower())
        prefix = "<" if self.is_little_endian else ">"
        return f"{prefix}{code}"

    @property
    def size(self) -> int:
        if self.type.lower().startswith("string"):
            return int(self.type.lower().replace("string", ""))

        return struct.calcsize(self.struct_format)

    def format(self) -> str:
        if self.value is None:
            return "-"

        if isinstance(self.value, int):
            type_lower = self.type.lower()
            if type_lower in ("int8", "int16", "int32", "int64"):
                return f"{self.value}"
            elif type_lower == "uint8":
                return f"{self.value} | 0x{self.value:02X}"
            elif type_lower == "binary":
                return f"{self.value:08b}"

            return f"{self.value} | 0x{self.value:X}"

        if isinstance(self.value, float):
            return f"{self.value:.4f}"

        return str(f"'{self.value}'")

    def edit_format(self) -> str:
        if self.type.lower() == "uint8":
            return f"{self.value}"

        return self.format()

    def set_value(self, data: bytes | memoryview):
        if self.offset + self.size <= len(data):
            if self.type.lower().startswith("string"):
                self.value = str(data[self.offset:self.offset + self.size], encoding="ascii", errors="replace")
            else:
                value = struct.unpack_from(self.struct_format, data, self.offset)[0]
                self.value = value
        else:
            # Not enough data for this field
            self.value = None

    def update_value_from_string(self, value_str: str) -> bytes:
        type_lower = self.type.lower()
        if type_lower.startswith("string"):
            encoded = value_str.encode("ascii", errors="replace")
            return encoded.ljust(self.size, b"\x00")[:self.size]
        elif type_lower in ("float", "double"):
            val = float(value_str)
            return struct.pack(self.struct_format, val)
        elif type_lower == "binary":
            try:
                val = int(value_str, 2)
            except ValueError:
                # Allow updating binary fields with decimal/hex values
                val = int(value_str, 0)
            return struct.pack(self.struct_format, val)
        else:
            val = int(value_str, 0)
            return struct.pack(self.struct_format, val)


@dataclass
class Schema:
    name: str
    fields: List[Field] = field(default_factory=list)

    def __post_init__(self):
        current_offset = 0
        for f in self.fields:
            f.offset = current_offset
            current_offset += f.size

    def parse(self, data: bytes | memoryview):
        for f in self.fields:
            f.set_value(data)
