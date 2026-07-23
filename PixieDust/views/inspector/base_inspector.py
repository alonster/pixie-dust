from textual import events
from textual.containers import Vertical
from textual.message import Message
from PixieDust.utils.data_manager import DataManager
from PixieDust.utils.schema import Field
from PixieDust.views.inspector.editable_field import InlineInput
from PixieDust.utils.styles import Color


class BaseInspectorView(Vertical):
    class EditEnded(Message):
        pass

    def __init__(self, data_manager: DataManager):
        super().__init__()
        self.data_manager = data_manager
        self.field_widgets = []  # List of (Field, EditableField)
        self.selected_index = 0
        self.is_focused_view = False

    def get_selected_field(self) -> Field | None:
        if 0 <= self.selected_index < len(self.field_widgets):
            return self.field_widgets[self.selected_index][0]
        return None

    def handle_key_event(self, event: events.Key) -> None:
        if any(widget.is_editing for _, widget in self.field_widgets):
            return

        if event.key in ("up", "down"):
            event.stop()
            if event.key == "up":
                self.selected_index = max(0, self.selected_index - 1)
            else:
                self.selected_index = min(len(self.field_widgets) - 1, self.selected_index + 1)
            self.refresh_highlight(is_focused=True)
            field, _ = self.field_widgets[self.selected_index]
            self.data_manager.current_pos = field.offset
            self.data_manager.active_field = field
        elif event.key == "enter":
            event.stop()
            field, widget = self.field_widgets[self.selected_index]
            widget.start_edit(field.edit_format())

    def refresh_highlight(self, is_focused: bool) -> None:
        self.is_focused_view = is_focused
        self._apply_widget_styles()

    def _apply_widget_styles(self) -> None:
        for index, (_, widget) in enumerate(self.field_widgets):
            if index == self.selected_index:
                widget.styles.background = Color.mediumpurple
                widget.static_val.styles.text_style = "bold"
            else:
                widget.styles.background = Color.deep_grey
                widget.static_val.styles.text_style = "none"

    def on_input_submitted(self, event: InlineInput.Submitted) -> None:
        event.stop()
        for field, widget in self.field_widgets:
            if widget.input_val == event.input:
                new_val = event.value
                try:
                    new_bytes = field.update_value_from_string(new_val)
                    self.data_manager.update_data_range(field.offset, new_bytes)
                    self.notify(f"Updated {field.name} -> {new_val}", severity="information")
                except Exception as e:
                    self.notify(f"Invalid input: {e}", severity="error")
                widget.end_edit()
                self.post_message(self.EditEnded())
                break

    def on_inline_input_cancel_edit(self, event: InlineInput.CancelEdit) -> None:
        event.stop()
        for _, widget in self.field_widgets:
            if widget.input_val == event.sender:
                widget.end_edit()
                self.post_message(self.EditEnded())
                break
