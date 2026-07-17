import pytest
from pathlib import Path

from PixieDust.app import PixieDust
from PixieDust.utils.file_manager import FileManager


@pytest.fixture
def app():
    FileManager.set_path(Path('demo.bin'))
    return PixieDust()
