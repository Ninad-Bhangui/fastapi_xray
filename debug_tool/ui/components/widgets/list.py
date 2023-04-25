from commons.logger import get_logger
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Label, ListItem, ListView

logger = get_logger(__name__)


class LabelItem(ListItem):
    DEFAULT_CSS = """
        ListItem {
            color: $text;
            height: auto;
            background: #68625d;
            overflow: hidden hidden;
        }
        ListItem > Widget :hover {
            background: $boost;
        }
        ListView > ListItem.--highlight {
            background: #7b7263 50%;
        }
        ListView:focus > ListItem.--highlight {
            background: #5f6062;
        }
        ListItem > Widget {
            height: auto;
        }
        """

    def __init__(self, label: str, value: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.label = label
        self.value = value

    def compose(self) -> ComposeResult:
        yield Label(self.label, classes="left_panel_label")


class ListItems(ListView):
    items = reactive([])

    def __init__(self, **kwargs):
        super().__init__(id="left_panel_list_view", **kwargs)
