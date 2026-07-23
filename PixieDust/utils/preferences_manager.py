from dataclasses import dataclass


@dataclass
class PreferenceOption:
    key: str
    label: str
    default: bool = False


class PreferencesManager:
    OPTIONS: list[PreferenceOption] = [
        PreferenceOption("binary_strict", "Strict Binary Parsing (01000001 only)", default=False),
        PreferenceOption("string_overflow", "Allow String Truncation (When too long)", default=True),
    ]
    _values: dict[str, bool] = {opt.key: opt.default for opt in OPTIONS}

    def __class_getitem__(cls, key: str) -> bool:
        return cls._values.get(key, False)

    @classmethod
    def set(cls, key: str, val: bool) -> None:
        cls._values[key] = val

    @classmethod
    def reset_defaults(cls) -> None:
        cls._values = {opt.key: opt.default for opt in cls.OPTIONS}
