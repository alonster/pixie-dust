import click
import pathlib

from PixieDust.utils.file_manager import FileManager
from PixieDust.utils.schema_manager import SchemaManager
from PixieDust.app import PixieDust


@click.command(name='pixie-dust')
@click.argument('file-name', type=click.Path(exists=True))
@click.option('--schema', '-s', type=click.Path(exists=True), help='Path to the YAML schema file')
def main(file_name: str, schema: str | None = None):
    file_path = pathlib.Path(click.format_filename(file_name))
    FileManager.set_path(file_path)

    if schema:
        schema_path = pathlib.Path(click.format_filename(schema))
        SchemaManager.set_path(schema_path)

    app = PixieDust()
    app.run()

if __name__ == '__main__':
    main()
