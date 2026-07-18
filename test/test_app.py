import pytest
import pathlib
import unittest.mock as mock
from click.testing import CliRunner

from PixieDust.cli import main
from PixieDust.utils.file_manager import FileManager
from PixieDust.utils.schema_manager import SchemaManager
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


@pytest.mark.asyncio
async def test_schema_navigation_syncs_cursor(app):
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

        # Initially, current pos is 0
        assert app.hex_view.data_manager.current_pos == 0

        # Press down (moves from Magic [offset 0, size 4] to Version [offset 4])
        await pilot.press("down")
        assert app.hex_view.data_manager.current_pos == 4

        # Press down (moves to Flags [offset 6])
        await pilot.press("down")
        assert app.hex_view.data_manager.current_pos == 6


@pytest.mark.asyncio
async def test_cancel_exit_when_editing(app):
    async with app.run_test() as pilot:
        assert app.hex_view.active_section == ActiveSection.NONE

        # Toggle on
        await pilot.press("e")

        # Try to quit
        await pilot.press("q")

        # Press right arrow to cancel
        await pilot.press("right")
        await pilot.press("enter")

        # Make sure app is still running
        assert app.is_running


@pytest.mark.asyncio
async def test_app_loads_custom_yaml_schema(app):
    async with app.run_test() as pilot:
        # Enter edit mode
        await pilot.press("e")
        # Cycle to inspector
        await pilot.press("tab")
        await pilot.press("tab")
        # Toggle mode to schema tab
        await pilot.press("m")

        schema_view = app.hex_view.inspector.schema_view
        assert schema_view.schema.name == "Demo Schema"
        assert len(schema_view.schema.fields) == 6


def test_cli_file_and_schema_arguments(tmp_path):
    dummy_bin = tmp_path / "dummy.bin"
    dummy_bin.write_bytes(b"\x00" * 32)

    dummy_yaml = tmp_path / "dummy.yaml"
    dummy_yaml.write_text("""
name: "CLI Mock Schema"
fields:
  - name: "DummyField"
    type: "uint8"
""")

    with mock.patch("PixieDust.cli.PixieDust") as MockApp:
        runner = CliRunner()
        result = runner.invoke(main, [str(dummy_bin), "--schema", str(dummy_yaml)])

        assert result.exit_code == 0
        assert FileManager.get_path() == dummy_bin
        assert SchemaManager.get_path() == dummy_yaml
        MockApp.assert_called_once()
