##
#
#  This example subscribes the all characters death events on the SolTech server, and
#  handles 20 events before exiting.
#  Output is in the adjacent NDJSON file.
#
##

from ps2_census import CharacterEvent, EventStream, EventStreamWorld, GenericCharacter


async def main():
    stream: EventStream = await EventStream()

    await stream.subscribe(
        worlds=[EventStreamWorld.SOLTECH],
        events=[CharacterEvent.DEATH],
        characters=[GenericCharacter.ALL],
    )

    events_count: int = 0
    while events_count < 20:
        print(await stream.receive())
        events_count += 1

    await stream.clear_all_subscriptions()
    await stream.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
