import pytest
from PixieDust.views.modals.goto_modal import GoToOffsetModal


def test_goto_modal_parses_hex_and_decimal_inputs():
    modal = GoToOffsetModal(max_offset=255)

    assert modal.parse_offset("0x10") == 16
    assert modal.parse_offset("0x1A") == 26
    assert modal.parse_offset("100") == 100
    assert modal.parse_offset("0") == 0
    assert modal.parse_offset("255") == 255

    # Out of bounds & invalid strings
    assert modal.parse_offset("256") is None
    assert modal.parse_offset("-5") is None
    assert modal.parse_offset("invalid") is None


@pytest.mark.asyncio
async def test_app_goto_offset_shortcut(app):
    async with app.run_test() as pilot:
        # Press 'g' to open GoToOffsetModal
        await pilot.press("g")
        assert any(isinstance(screen, GoToOffsetModal) for screen in app.screen_stack)

        # Type '0x10' and press enter
        await pilot.press("0", "x", "1", "0", "enter")

        # Verify cursor position moved to offset 16 (0x10)
        assert app.hex_view.data_manager.current_pos == 16
