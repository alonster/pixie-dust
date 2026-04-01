from enum import Enum

class ActiveSection(Enum):
    NONE = 0
    Hex = "Hex"
    ASCII = "ASCII"
    Inspector = "Inspector"

    def is_editable(self):
        return self.value != ActiveSection.NONE
