import pytest
from PixieDust.views.hex_row import HexRow
from PixieDust.utils.enums import ActiveSection, EditMode
from PixieDust.utils.schema import Field


@pytest.mark.asyncio
async def test_navigation_updates_position(app):
    async with app.run_test() as pilot:
        grid = app.hex_view.grid
        assert grid.data_manager.current_pos == 0

        await pilot.press("right")
        assert grid.data_manager.current_pos == 1

        await pilot.press("down")
        assert grid.data_manager.current_pos == 17


@pytest.mark.asyncio
async def test_hex_view_initialization(app):
    demo_file_length = 256

    async with app.run_test():
        assert len(app.hex_view.data_manager._data) == demo_file_length
        assert app.hex_view.has_unsaved_changes is False


@pytest.mark.asyncio
async def test_edit_hex_section(app):
    async with app.run_test() as pilot:
        grid = app.hex_view.grid
        await pilot.press("e")
        await pilot.press("1")
        assert grid.data_manager.get_data()[0] == 0x1

        await pilot.press("a")
        assert grid.data_manager.get_data()[0] == 0x1a

        await pilot.press("2")
        assert grid.data_manager.get_data()[1] == 0x2


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["1", "2", "a"])
async def test_edit_ascii_section(app, key):
    async with app.run_test() as pilot:
        grid = app.hex_view.grid
        await pilot.press("e")
        await pilot.press("tab")
        await pilot.press(key)
        assert grid.data_manager.get_data()[0] == ord(key)

        await pilot.press(key)
        assert grid.data_manager.get_data()[1] == ord(key)


def test_hex_row_field_highlight_rendering():
    row = HexRow(offset=0, data=memoryview(b"\x00" * 16))
    row.active_field = Field("Magic", "uint32", offset=0)

    text = row.render_section(ActiveSection.Hex)
    assert any("#36294c" in str(span.style) for span in text.spans)


def test_hex_row_eof_blinking_cursor_rendering():
    # Empty/partially filled row (4 bytes of data, 12 padding slots)
    row = HexRow(offset=0, data=memoryview(b"1234"))
    row.selected_column = 4  # Pointing to EOF position at padding index 4
    row.active_section = ActiveSection.Hex

    text = row.render_section(ActiveSection.Hex)
    # Verify blinking style is rendered for EOF cursor ++
    assert any("blink" in str(span.style) for span in text.spans)
    assert "++" in text.plain


@pytest.mark.asyncio
async def test_hex_grid_mounts_new_rows_when_data_expands(app):
    async with app.run_test() as pilot:
        grid = app.hex_view.grid
        initial_row_count = len(grid.query(HexRow))

        # Set DataManager to APPEND mode and append bytes beyond current row capacity
        grid.data_manager.edit_mode = EditMode.APPEND
        # Set pos to last index of current rows (16 rows * 16 bytes = 256 bytes)
        grid.data_manager.current_pos = len(grid.data_manager._data)

        # Append 16 new bytes (filling a brand new 17th row)
        grid.data_manager.update_data_range(len(grid.data_manager._data), b"A" * 16)
        await pilot.pause()

        # Verify dynamic row mounting
        new_row_count = len(grid.query(HexRow))
        assert new_row_count == initial_row_count + 1
