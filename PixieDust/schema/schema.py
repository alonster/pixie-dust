import struct
from dataclasses import dataclass, field
from typing import List, Any, Dict


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
        return struct.calcsize(self.struct_format)


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
            if f.offset + f.size <= len(data):
                val = struct.unpack_from(f.struct_format, data, f.offset)[0]
                f.value = val
            else:
                # Not enough data for this field
                f.value = None
