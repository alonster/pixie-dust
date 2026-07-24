import click
import pathlib

from PixieDust.app import PixieDust


@click.command(name='pixie-dust')
@click.argument('file-name', type=click.Path(exists=True))
@click.option('--schema', '-s', type=click.Path(exists=True), help='Path to the YAML schema file')
def main(file_name: str, schema: str | None = None):
    file_path = pathlib.Path(click.format_filename(file_name))
    schema_path = pathlib.Path(click.format_filename(schema)) if schema else None

    app = PixieDust(file_path=file_path, schema_path=schema_path)
    app.run()


if __name__ == '__main__':
    main()
