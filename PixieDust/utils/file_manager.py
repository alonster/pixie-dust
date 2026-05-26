from pathlib import Path


class FileManager:
    _FILE_PATH = Path()

    @staticmethod
    def set_path(file_path: Path):
        FileManager._FILE_PATH = file_path

    @staticmethod
    def get_path() -> Path:
        return FileManager._FILE_PATH

    @staticmethod
    def get_file_name() -> str:
        return FileManager.get_path().name

    @staticmethod
    def read_data_from_file():
        with open(FileManager.get_path(), "rb") as f:
            return bytearray(f.read())

    @staticmethod
    def save_data_to_file(data: bytearray):
        with open(FileManager.get_path(), "wb") as f:
            f.write(data)
