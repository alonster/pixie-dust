import pytest


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
