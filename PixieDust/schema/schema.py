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

    def parse(self, data: bytes) -> Dict[str, Any]:
        results = {}
        offset = 0
        for f in self.fields:
            if offset + f.size <= len(data):
                val = struct.unpack_from(f.struct_format, data, offset)[0]
                results[f.name] = val
                offset += f.size
            else:
                # Not enough data for this field
                results[f.name] = None
        return results
