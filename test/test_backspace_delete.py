import pytest
from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.enums import EditMode


def test_insert_mode_backspace_zeroes_preceding_byte():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    dm.edit_mode = EditMode.INSERT
    dm.current_pos = 3

    dm.remove_byte(at_current=False)

    assert len(dm._data) == 10
    assert dm.current_pos == 2
    assert dm._data == bytearray(b"01\x003456789")


def test_insert_mode_delete_zeroes_current_byte():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    dm.edit_mode = EditMode.INSERT
    dm.current_pos = 3

    dm.remove_byte(at_current=True)

    assert len(dm._data) == 10
    assert dm.current_pos == 3
    assert dm._data == bytearray(b"012\x00456789")


def test_append_mode_backspace_removes_preceding_byte():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    dm.edit_mode = EditMode.APPEND
    dm.current_pos = 3

    dm.remove_byte(at_current=False)

    assert len(dm._data) == 9
    assert dm.current_pos == 2
    assert dm._data == bytearray(b"013456789")


def test_append_mode_delete_removes_current_byte():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    dm.edit_mode = EditMode.APPEND
    dm.current_pos = 3

    dm.remove_byte(at_current=True)

    assert len(dm._data) == 9
    assert dm.current_pos == 3
    assert dm._data == bytearray(b"012456789")


def test_backspace_at_position_zero_does_nothing():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    dm.edit_mode = EditMode.APPEND
    dm.current_pos = 0

    dm.remove_byte(at_current=False)

    assert len(dm._data) == 10
    assert dm.current_pos == 0


@pytest.mark.asyncio
async def test_app_handles_backspace_and_delete_keys(app):
    async with app.run_test() as pilot:
        await pilot.press("e")
        app.hex_view.data_manager.current_pos = 2

        # Press backspace in INSERT mode -> zeroes byte 1
        await pilot.press("backspace")
        assert app.hex_view.data_manager.current_pos == 1
        assert app.hex_view.data_manager.get_data()[1] == 0

        # Toggle to APPEND mode
        await pilot.press("ctrl+a")
        assert app.hex_view.data_manager.edit_mode == EditMode.APPEND

        # Press delete in APPEND mode -> removes byte at index 1
        init_len = len(app.hex_view.data_manager.get_data())
        await pilot.press("delete")
        assert len(app.hex_view.data_manager.get_data()) == init_len - 1
