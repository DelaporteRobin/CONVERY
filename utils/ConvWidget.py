from __future__ import annotations

from typing import ClassVar, Iterable, Optional

from typing_extensions import TypeGuard

from textual.app import App, ComposeResult
from textual.widgets import Tree, ProgressBar, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.screen import Screen 
from textual.await_complete import AwaitComplete
from textual.await_remove import AwaitRemove
from textual.binding import Binding, BindingType
from textual import events
from textual import work
from textual.containers import Horizontal, Vertical, Container, VerticalScroll
from textual import on
from textual.events import Mount
from textual.message import Message
from textual.reactive import reactive
from textual.await_complete import AwaitComplete 
from textual.widgets._directory_tree import DirEntry
from textual.widgets._tree import TreeNode
from textual.errors import TextualError
from textual.widgets._list_item import ListItem
from textual.widget import AwaitMount, Widget







class MultiListItem(ListItem):
    """A widget that is an item within a `ListView`.

    A `ListItem` is designed for use within a
    [ListView][textual.widgets._list_view.ListView], please see `ListView`'s
    documentation for more details on use.
    """ 

    #highlighted = reactive(False)
    highlight_list = []
    """Is this item highlighted?"""

    def watch_highlighted(self, value: bool) -> None:
        #self.notify(str(self in self.highlight_list))

        #self.notify(str(self.classes))

        if "separator" in self.classes:
            return

        if self in self.highlight_list:
            self.set_class(True, "-highlight")
        else:
            self.set_class(value, "-highlight")
        
        """
        conditions to highlight an object
        1 - current object selected
        2 - object in the list
        """

    def highlight_item(self, item) -> None:
        #self.notify(str(item))
        if item not in self.highlight_list:
            self.highlight_list.append(item)
            self.highlighted=True
        else:
            self.highlight_list.remove(item)
            self.highlighted = False

        for element in self.highlight_list:
            element.highlighted = True

    @on(events.Enter)
    @on(events.Leave)
    def on_enter_or_leave(self, event: events.Enter | events.Leave) -> None:
        event.stop()
        self.set_class(self.is_mouse_over, "-hovered")



class MultiListView(ListView):
    #reactive to share index_list with all instances
    #index_list = reactive[list]([], init=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_list = []

    @property
    def highlighted_child(self) -> ListItem | None:
        """The currently highlighted ListItem, or None if nothing is highlighted."""
        if self.index is not None and 0 <= self.index < len(self._nodes):
            list_item = self._nodes[self.index]

            #self.notify(str(list_item.classes))
            #self.notify(str("separator" in list_item.classes))

            if self.index not in self.index_list:
                self.index_list.append(self.index)
            else:
                self.index_list.remove(self.index)

            #self.notify(str(self.index_list))


            assert isinstance(list_item, ListItem)
            return list_item
        else:
            return None



    def clear_list(self) -> ListItem | None:
        self.index_list.clear()



