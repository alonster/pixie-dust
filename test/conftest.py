import pytest
from pathlib import Path

from PixieDust.app import PixieDust
from PixieDust.utils.file_manager import FileManager
from PixieDust.utils.schema_manager import SchemaManager


@pytest.fixture
def app():
    FileManager.set_path(Path('demo.bin'))
    yaml_path = Path(__file__).parent / "sample_schema.yaml"
    SchemaManager.set_path(yaml_path)
    return PixieDust()
