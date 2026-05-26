import click
import pathlib

from PixieDust.utils.file_manager import FileManager


from PixieDust.app import PixieDust


@click.command(name='pixie-dust')
@click.argument('file-name', type=click.Path(exists=True))
def main(file_name: str):
    file_path = pathlib.Path(click.format_filename(file_name))
    FileManager.set_path(file_path)
    app = PixieDust()
    app.run()

if __name__ == '__main__':
    main()
