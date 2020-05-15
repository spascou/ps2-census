import logging
from copy import deepcopy
from typing import Dict, List, Literal, Optional, Tuple, Union

import requests
import requests.exceptions
import urllib3.exceptions
from tenacity import (
    after_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .constants import (
    CENSUS_ENDPOINT,
    EXAMPLE_SERVICE_ID,
    FIELD_SEPARATOR,
    SERVICE_ID_PREFIX,
    Collection,
    Command,
    Namespace,
    SearchModifier,
    Verb,
)
from .join import Join
from .tree import Tree
from .utils import bool2str, command_key

logger = logging.getLogger(__name__)


class Query:
    collection: Collection
    endpoint: str
    service_id: str
    namespace: Namespace
    parameters: Dict[str, List[str]]

    def __init__(
        self,
        collection: Collection,
        endpoint: str = CENSUS_ENDPOINT,
        service_id: str = EXAMPLE_SERVICE_ID,
        namespace: Namespace = Namespace.PS2_V2,
    ):
        self.collection = collection
        self.endpoint = endpoint
        self.service_id = service_id
        self.namespace = namespace
        self.parameters = {}

    def _add_parameter(self, key: str, value: Union[str, int]):
        key = f"{key}"
        value = f"{value}"

        if key not in self.parameters:
            self.parameters[key] = [value]
        else:
            self.parameters[key].append(value)

    def __eq__(self, other):
        if isinstance(other, Query):
            return (
                self.collection == other.collection
                and self.endpoint == other.endpoint
                and self.service_id == other.service_id
                and self.namespace == other.namespace
                and self.parameters == other.parameters
            )

        return False

    def set_service_id(self, service_id: str):
        self.service_id = service_id
        return self

    def get_factory(self):
        self_copy = deepcopy(self)

        def factory():
            return deepcopy(self_copy)

        return factory

    def _get_url(self, verb: Verb) -> str:
        return f"{self.endpoint}/{SERVICE_ID_PREFIX}{self.service_id}/{verb}/{self.namespace}/{self.collection}"

    def _execute_query(self, verb: Verb) -> requests.Response:
        res: requests.Response = requests.get(
            self._get_url(verb), params=self.parameters
        )
        res.raise_for_status()

        return res

    @retry(
        retry=(
            retry_if_exception_type(ConnectionError)
            | retry_if_exception_type(requests.exceptions.ConnectionError)
            | retry_if_exception_type(urllib3.exceptions.ProtocolError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(),
        after=after_log(logger, logging.DEBUG),
    )
    def get(self) -> dict:
        res: requests.Response = self._execute_query(Verb.GET)
        return res.json()

    @retry(
        retry=(
            retry_if_exception_type(ConnectionError)
            | retry_if_exception_type(requests.exceptions.ConnectionError)
            | retry_if_exception_type(urllib3.exceptions.ProtocolError)
        ),
        stop=stop_after_attempt(5),
        wait=wait_exponential(),
        after=after_log(logger, logging.DEBUG),
    )
    def count(self) -> dict:
        res: requests.Response = self._execute_query(Verb.COUNT)
        return res.json()

    def filter(
        self,
        field: str,
        value: Union[str, int],
        modifier: Optional[SearchModifier] = None,
    ):
        self._add_parameter(field, value if modifier is None else f"{modifier}{value}")
        return self

    def show(self, *args: str):
        key = command_key(Command.SHOW)
        self._add_parameter(key, FIELD_SEPARATOR.join(args))
        return self

    def hide(self, *args: str):
        key = command_key(Command.HIDE)
        self._add_parameter(key, FIELD_SEPARATOR.join(args))
        return self

    def sort(self, *args: Tuple[str, Literal[1, -1]]):
        key = command_key(Command.SORT)
        value = FIELD_SEPARATOR.join((f"{a[0]}:{a[1]}" for a in args))
        self._add_parameter(key, value)
        return self

    def has(self, *args: str):
        key = command_key(Command.HAS)
        self._add_parameter(key, FIELD_SEPARATOR.join(args))
        return self

    def case(self, arg: bool):
        key = command_key(Command.CASE)
        self._add_parameter(key, bool2str(arg))
        return self

    def limit(self, arg: int):
        key = command_key(Command.LIMIT)
        self._add_parameter(key, arg)
        return self

    def limit_per_db(self, arg: int):
        key = command_key(Command.LIMIT_PER_DB)
        self._add_parameter(key, arg)
        return self

    def start(self, arg: int):
        key = command_key(Command.START)
        self._add_parameter(key, arg)
        return self

    def include_null(self, arg: bool):
        key = command_key(Command.INCLUDE_NULL)
        self._add_parameter(key, bool2str(arg))
        return self

    def lang(self, arg: str):
        key = command_key(Command.LANG)
        self._add_parameter(key, arg)
        return self

    def join(self, arg: Join):
        key = command_key(Command.JOIN)
        self._add_parameter(key, arg.__str__())
        return self

    def tree(self, arg: Tree):
        key = command_key(Command.TREE)
        self._add_parameter(key, arg.__str__())
        return self

    def timing(self, arg: bool):
        key = command_key(Command.TIMING)
        self._add_parameter(key, bool2str(arg))
        return self

    def exact_match_first(self, arg: bool):
        key = command_key(Command.EXACT_MATCH_FIRST)
        self._add_parameter(key, bool2str(arg))
        return self

    def distinct(self, arg: str):
        key = command_key(Command.DISTINCT)
        self._add_parameter(key, arg)
        return self

    def retry(self, arg: bool):
        key = command_key(Command.RETRY)
        self._add_parameter(key, bool2str(arg))
        return self
