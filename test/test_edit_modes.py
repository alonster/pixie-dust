import pytest
from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.enums import EditMode


def test_default_insert_mode_modifies_in_place():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    # Hold active memoryview (simulating mounted UI views)
    view = dm.get_data()
    assert view[0] == ord("0")

    dm.edit_mode = EditMode.INSERT
    dm.current_pos = 2

    # Overwrite in-place at index 2
    dm.update_byte(ord("X"))

    assert len(dm._data) == 10
    assert dm._data == bytearray(b"01X3456789")


def test_append_mode_inserts_at_exact_position():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    # Hold active memoryview (simulating mounted UI views)
    view = dm.get_data()
    assert view[0] == ord("0")

    dm.edit_mode = EditMode.APPEND
    dm.current_pos = 2

    # Append (splice) byte 'X' at index 2
    dm.update_byte(ord("X"))

    assert len(dm._data) == 11
    # Verify index 2 is 'X', preceding bytes (0..1) intact, trailing bytes (2..9) shifted right
    assert dm._data[2] == ord("X")
    assert dm._data[:2] == bytearray(b"01")
    assert dm._data[3:] == bytearray(b"23456789")
    assert dm._data == bytearray(b"01X23456789")


def test_append_mode_at_eof():
    dm = DataManager()
    dm._data = bytearray(b"0123456789")
    # Hold active memoryview (simulating mounted UI views)
    view = dm.get_data()
    assert view[0] == ord("0")

    dm.edit_mode = EditMode.APPEND
    dm.current_pos = 10  # At EOF

    dm.update_byte(ord("Z"))

    assert len(dm._data) == 11
    assert dm._data == bytearray(b"0123456789Z")


@pytest.mark.asyncio
async def test_app_toggles_edit_mode_and_edits_in_append_mode(app):
    async with app.run_test() as pilot:
        initial_length = len(app.hex_view.data_manager._data)

        # Enter Edit mode
        await pilot.press("e")
        assert app.hex_view.grid.active_section.is_editable()
        assert app.hex_view.data_manager.edit_mode == EditMode.INSERT
        assert "INSERT" in app.title

        # Toggle to APPEND mode with 'ctrl+a'
        await pilot.press("ctrl+a")
        assert app.hex_view.data_manager.edit_mode == EditMode.APPEND
        assert "APPEND" in app.title

        # Type two hex characters ("f" and "f") in APPEND mode to edit a byte on running UI
        await pilot.press("f")
        await pilot.press("f")

        # Verify size grew by exactly 1 byte (for 2 typed hex nibbles) without BufferError
        assert len(app.hex_view.data_manager._data) == initial_length + 1

        # Toggle back to INSERT mode with 'ctrl+a'
        await pilot.press("ctrl+a")
        assert app.hex_view.data_manager.edit_mode == EditMode.INSERT
        assert "INSERT" in app.title


@pytest.mark.asyncio
async def test_eof_navigation_in_append_mode_does_not_raise_index_error(app):
    async with app.run_test() as pilot:
        await pilot.press("e")
        await pilot.press("ctrl+a")
        assert app.hex_view.data_manager.edit_mode == EditMode.APPEND

        # Move current_pos to EOF (past last byte index)
        app.hex_view.data_manager.current_pos = len(app.hex_view.data_manager._data)

        # Trigger schema inspector update_info at EOF position without IndexError
        raw_field = app.hex_view.inspector.schema_view.update_info(
            app.hex_view.data_manager.get_data(),
            app.hex_view.data_manager.current_pos
        )
        assert raw_field.offset == len(app.hex_view.data_manager._data)
