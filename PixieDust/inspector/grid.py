from textual.app import ComposeResult
from textual.containers import Grid
from textual.widgets import Label, Static
from PixieDust.styles import Color

class KeyValueGrid(Grid):
    def on_mount(self) -> None:
        self.styles.padding = (0, 1)
        self.styles.grid_size_columns = 2
        self.styles.grid_columns = "10 1fr"
        self.styles.grid_gutter_vertical = 1
        self.styles.grid_gutter_horizontal = 1
        self.styles.height = "auto"

    @staticmethod
    def add_pair(key: str, value: Static) -> ComposeResult:
        label = Label(f"{key}:")
        
        # Style the Label (Key)
        label.styles.color = Color.orange
        label.styles.content_align = ("right", "middle")
        
        # Style the static value
        value.styles.background = Color.deep_grey
        value.styles.color = Color.white
        value.styles.border_left = ("solid", Color.mediumpurple)
        value.styles.padding = (0, 1)
        
        yield label
        yield value
