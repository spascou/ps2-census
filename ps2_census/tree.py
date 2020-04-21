from typing import Literal, Union

from .constants import TREE_ITEM_DELIMITER, TreeKey


class Tree:
    items: dict

    def __init__(self, field: str):
        self.items = {}

        self._add_item(TreeKey.FIELD, field)

    def __str__(self) -> str:
        return TREE_ITEM_DELIMITER.join((f"{k}:{v}" for k, v in self.items.items()))

    def _add_item(self, key: TreeKey, value: Union[str, int]):
        self.items[key.value] = value

    def list(self, arg: Literal[1, 0]):
        self._add_item(TreeKey.LIST, arg)
        return self

    def prefix(self, arg: str):
        self._add_item(TreeKey.PREFIX, arg)
        return self

    def start(self, arg: str):
        self._add_item(TreeKey.START, arg)
        return self
