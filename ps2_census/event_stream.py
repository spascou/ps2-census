import json
import sys
from typing import List, Optional, Union

import websockets

from .constants import (
    EXAMPLE_SERVICE_ID,
    PUSH_ENDPOINT,
    CharacterEvent,
    GenericEvent,
    EventStreamAction,
    EventStreamService,
    EventStreamWorld,
    Namespace,
    WorldEvent,
)
from .utils import service_id_key


class EventStream(object):
    endpoint: str
    service_id: str
    namespace: Namespace

    def __init__(
        self,
        endpoint: str = PUSH_ENDPOINT,
        service_id: str = EXAMPLE_SERVICE_ID,
        namespace: Namespace = Namespace.PS2,
    ):
        self.endpoint = endpoint
        self.service_id = service_id_key(service_id)
        self.namespace = namespace

    def __await__(self):
        return self._async_init().__await__()

    def _get_url(self) -> str:
        return (
            f"{self.endpoint}?environment={self.namespace}&service-id={self.service_id}"
        )

    async def _async_init(self):
        self._conn = websockets.connect(self._get_url())
        self.websocket = await self._conn.__aenter__()
        return self

    async def close(self):
        await self._conn.__aexit__(*sys.exc_info())

    async def receive(self):
        return json.loads(await self.websocket.recv())

    async def echo(self):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.ECHO.value,
            "payload": {"test": "test"},
        }

        await self.websocket.send(json.dumps(message))

    async def subscribe(
        self,
        worlds: Optional[List[EventStreamWorld]] = None,
        characters: Optional[List[str]] = None,
        events: Optional[List[Union[GenericEvent, WorldEvent, CharacterEvent]]] = None,
        logical_and_characters_with_worlds: bool = False,
    ):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.SUBSCRIBE.value,
        }

        if worlds:
            message["worlds"] = [w.value for w in worlds]
        if characters:
            message["characters"] = characters
        if events:
            message["eventNames"] = [e.value for e in events]
        if logical_and_characters_with_worlds is True:
            message["logicalAndCharactersWithWorlds"] = "true"

        await self.websocket.send(json.dumps(message))

    async def clear_subscriptions(
        self,
        worlds: Optional[List[EventStreamWorld]] = None,
        characters: Optional[List[str]] = None,
        events: Optional[List[Union[WorldEvent, CharacterEvent]]] = None,
        logical_and_characters_with_worlds: bool = False,
    ):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.CLEAR_SUBSCRIBE.value,
        }

        if worlds:
            message["worlds"] = [w.value for w in worlds]
        if characters:
            message["characters"] = characters
        if events:
            message["eventNames"] = [e.value for e in events]
        if logical_and_characters_with_worlds is True:
            message["logicalAndCharactersWithWorlds"] = "true"

        await self.websocket.send(json.dumps(message))

    async def clear_all_subscriptions(self):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.CLEAR_SUBSCRIBE.value,
            "all": "true",
        }

        await self.websocket.send(json.dumps(message))

    async def recent_character_ids(self):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.RECENT_CHARACTER_IDS.value,
        }

        await self.websocket.send(json.dumps(message))

    async def recent_character_ids_count(self):
        message: dict = {
            "service": EventStreamService.EVENT.value,
            "action": EventStreamAction.RECENT_CHARACTER_IDS_COUNT.value,
        }

        await self.websocket.send(json.dumps(message))
