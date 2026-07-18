from pathlib import Path


class SchemaManager:
    _SCHEMA_PATH: Path | None = None

    @staticmethod
    def set_path(schema_path: Path | None):
        SchemaManager._SCHEMA_PATH = schema_path

    @staticmethod
    def get_path() -> Path | None:
        return SchemaManager._SCHEMA_PATH
