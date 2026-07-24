import pytest
from pathlib import Path

from PixieDust.app import PixieDust


@pytest.fixture
def app():
    demo_path = Path("demo.bin")
    yaml_path = Path(__file__).parent / "sample_schema.yaml"
    return PixieDust(file_path=demo_path, schema_path=yaml_path)
