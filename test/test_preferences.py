import pytest
from PixieDust.utils.preferences_manager import PreferencesManager
from PixieDust.utils.schema import Field


@pytest.fixture(autouse=True)
def reset_preferences():
    PreferencesManager.reset_defaults()
    yield
    PreferencesManager.reset_defaults()


def test_preferences_manager_get_and_set():
    assert PreferencesManager["binary_strict"] is False
    PreferencesManager.set("binary_strict", True)
    assert PreferencesManager["binary_strict"] is True


def test_binary_strict_preference():
    field = Field("Binary", "binary")

    # Default (Lenient): accepts decimal/hex
    res = field.update_value_from_string("65")
    assert res == b"\x41"

    # Strict mode: rejects non-binary digits
    PreferencesManager.set("binary_strict", True)
    with pytest.raises(ValueError, match="Binary string must contain only 0 and 1 digits"):
        field.update_value_from_string("65")

    # Strict mode: accepts valid 8-bit binary
    res_strict = field.update_value_from_string("01000001")
    assert res_strict == b"\x41"


def test_string_overflow_preference():
    field = Field("String", "string4")

    # Default: allows overflow
    res = field.update_value_from_string("HELLO WORLD")
    assert res == b"HELL"

    # Disallowed overflow: should throw
    PreferencesManager.set("string_overflow", False)
    with pytest.raises(ValueError, match="exceeds field capacity"):
        field.update_value_from_string("HELLO WORLD")
