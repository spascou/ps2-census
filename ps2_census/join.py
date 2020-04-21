from typing import Literal, Union

from .constants import JOIN_ITEM_DELIMITER, JOIN_VALUE_DELIMITER, Collection, JoinKey


class Join:
    items: dict
    collection: Collection

    def __init__(self, arg: Collection):
        self.collection = arg
        self.items = {}
        self.nested_join = None

    def __str__(self) -> str:
        res = JOIN_ITEM_DELIMITER.join(
            [f"{self.collection.value}"] + [f"{k}:{v}" for k, v in self.items.items()]
        )

        if self.nested_join:
            nested_res = self.nested_join.__str__()
            return f"{res}({nested_res})"
        else:
            return res

    def nest(self, other):
        assert isinstance(other, Join)
        self.nested_join = other
        return self

    def _add_item(self, key: JoinKey, value: Union[str, int]):
        self.items[f"{key.value}"] = f"{value}"

    def on(self, arg: str):
        self._add_item(JoinKey.ON, arg)
        return self

    def to(self, arg: str):
        self._add_item(JoinKey.TO, arg)
        return self

    def list(self, arg: Literal[1, 0]):
        self._add_item(JoinKey.LIST, arg)
        return self

    def show(self, *args: str):
        value = JOIN_VALUE_DELIMITER.join(args)
        self._add_item(JoinKey.SHOW, value)
        return self

    def hide(self, *args: str):
        value = JOIN_VALUE_DELIMITER.join(args)
        self._add_item(JoinKey.HIDE, value)
        return self

    def inject_at(self, arg: str):
        self._add_item(JoinKey.INJECT_AT, arg)
        return self

    def terms(self, **kwargs: Union[str, int]):
        self._add_item(
            JoinKey.TERMS,
            JOIN_VALUE_DELIMITER.join((f"{k}={v}" for k, v in kwargs.items())),
        )
        return self

    def outer(self, arg: Literal[1, 0]):
        self._add_item(JoinKey.OUTER, arg)
        return self
