import pytest

from PixieDust.utils.enums import ActiveSection


@pytest.mark.asyncio
async def test_edit_mode_toggle(app):
    async with app.run_test() as pilot:
        assert app.hex_view.active_section == ActiveSection.NONE

        # Toggle on
        await pilot.press("e")
        assert app.hex_view.active_section == ActiveSection.Hex

        # Toggle off
        await pilot.press("escape")
        assert app.hex_view.active_section == ActiveSection.NONE


@pytest.mark.asyncio
async def test_tab_cycling(app):
    async with app.run_test() as pilot:
        # Should start as None
        assert app.hex_view.active_section == ActiveSection.NONE

        # When entering edit-mode - should be Hex.
        await pilot.press("e")
        assert app.hex_view.active_section == ActiveSection.Hex

        await pilot.press("tab")
        assert app.hex_view.active_section == ActiveSection.ASCII

        await pilot.press("tab")
        assert app.hex_view.active_section == ActiveSection.Inspector

        await pilot.press("tab")
        assert app.hex_view.active_section == ActiveSection.Hex


@pytest.mark.asyncio
async def test_inspector_edit(app):
    async with app.run_test() as pilot:
        # Enter edit mode
        await pilot.press("e")
        # Cycle to inspector
        await pilot.press("tab")
        await pilot.press("tab")
        assert app.hex_view.active_section == ActiveSection.Inspector

        # Press enter to edit active field (Byte/U8)
        await pilot.press("enter")
        # Type value "66" (ASCII 'B')
        await pilot.press("6")
        await pilot.press("6")
        await pilot.press("enter")

        # Verify that the value was updated
        assert app.hex_view.data_manager.get_data()[0] == 66

        # Try to navigate down after edit
        await pilot.press("down")
        assert app.hex_view.inspector.raw_view.selected_index == 1


@pytest.mark.asyncio
async def test_schema_inspector_edit(app):
    async with app.run_test() as pilot:
        # Enter edit mode
        await pilot.press("e")
        # Cycle to inspector
        await pilot.press("tab")
        await pilot.press("tab")
        assert app.hex_view.active_section == ActiveSection.Inspector

        # Toggle mode to schema tab
        await pilot.press("m")
        assert app.hex_view.inspector.tabs.active == "schema"

        # Press enter to edit active field
        await pilot.press("enter")
        # Type value
        await pilot.press("1")
        await pilot.press("2")
        await pilot.press("enter")

        # Try to navigate down after edit
        assert app.focused == app.hex_view.inspector
        assert app.hex_view.data_manager.get_data()[0] == 12
        assert not app.hex_view.inspector.schema_view.field_widgets[0][1].is_editing
        await pilot.press("down")
        assert app.hex_view.inspector.schema_view.selected_index == 1
