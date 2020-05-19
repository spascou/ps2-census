import pytest
import websockets

from ps2_census import (
    CharacterEvent,
    EventStream,
    EventStreamWorld,
    GenericCharacter,
    GenericEvent,
)


async def mirror_server(ws, path):
    msg = await ws.recv()
    await ws.send(msg)


@pytest.mark.asyncio
async def test_connection():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    await stream.close()

    server.close()
    await server.wait_closed()


@pytest.mark.asyncio
async def test_send_and_receive():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        message: dict = {"somekey": "somevalue"}
        await stream.send(message)

        result: dict = await stream.receive()
        assert result == message

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_echo():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        message: dict = {"somekey": "somevalue"}
        await stream.echo(message)

        result: dict = await stream.receive()
        assert result == {
            "service": "event",
            "action": "echo",
            "payload": message,
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_subscribe_all():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.subscribe(
            worlds=(EventStreamWorld.ALL,),
            characters=(GenericCharacter.ALL,),
            events=(GenericEvent.ALL,),
            logical_and_characters_with_worlds=True,
        )

        assert await stream.receive() == {
            "service": "event",
            "action": "subscribe",
            "characters": ["all"],
            "worlds": ["all"],
            "eventNames": ["all"],
            "logicalAndCharactersWithWorlds": True,
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_subscribe_some():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.subscribe(characters=("1234",), events=(CharacterEvent.DEATH,))

        assert await stream.receive() == {
            "service": "event",
            "action": "subscribe",
            "characters": ["1234"],
            "eventNames": ["Death"],
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_clear_subscriptions():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.clear_subscriptions(
            worlds=(EventStreamWorld.BRIGGS,),
            characters=("1234",),
            events=(CharacterEvent.DEATH,),
            logical_and_characters_with_worlds=True,
        )

        assert await stream.receive() == {
            "service": "event",
            "action": "clearSubscribe",
            "worlds": ["25"],
            "characters": ["1234"],
            "eventNames": ["Death"],
            "logicalAndCharactersWithWorlds": True,
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_clear_all_subscriptions():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.clear_all_subscriptions()

        assert await stream.receive() == {
            "service": "event",
            "action": "clearSubscribe",
            "all": "true",
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_recent_character_ids():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.recent_character_ids()

        assert await stream.receive() == {
            "service": "event",
            "action": "recentCharacterIds",
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_recent_character_ids_count():
    server = await websockets.serve(mirror_server, "localhost", 8765)
    stream = await EventStream(
        endpoint="ws://localhost:8765", service_id="someserviceid"
    )

    try:
        await stream.recent_character_ids_count()

        assert await stream.receive() == {
            "service": "event",
            "action": "recentCharacterIdsCount",
        }

    finally:
        await stream.close()
        server.close()
        await server.wait_closed()
