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
