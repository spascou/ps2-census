# ps2-census

ps2-census is a low-level client for Daybreak's Planetside 2 Census API written in Python >= 3.8.

*Features*:
- Build queries through method chaining
- Join collections and nest them through method chaining
- Get raw (deserialized) responses as Python dictionaries
- Access common enums directly
- Subscribe to event streams

By default the `s:example` service ID is used; however it is not recommended for production.
You should get your own service ID from the webside below and supply it to the client whenever needed.

More information about the Census API is available on the official Census documentation [here](http://census.daybreakgames.com/).

[Iridar's blog](https://iridar-mirror.knyazev.io/index.html%3Fp=4127.html) is also recommended to understand
the quirks of this particular API as this knowledge is necessary to use ps2-census properly.

## Installation

`pip install ps2-census`

## Query building

Queries are made on collections with optional joins on other collections as well as various
commands that alter the output.

### Basic query

To build a query, instantiate the `Query` class with a `Collection` and your service ID:
```
from ps2_census import Collection, Query

query: Query = Query(Collection.ITEM, service_id=YOUR_SERVICE_ID)
```

Chain methods to alter the query further. Available methods are those detailed on the
official Census API documentation website.
```
query: Query = (
    Query(Collection.ITEM, service_id=YOUR_SERVICE_ID)
    .lang("en")
    .sort(("item_id", 1), ("faction_id", -1))
    .limit(30)
)
```

Execute the query in one of the 2 ways made available by the Census API:

- `.count()` to get the items count
```
query.count()
> {'count': 21048}
```

- `.get()` to get the results
```
query.get()
> {'item_list': [{...}, {...}, ...], 'returned': 30}
```

### Simple join

In order to perform joins instantiate the `Join` class with a `Collection` and pass it to the `Query`:
```
from ps2_census import Collection, Join, Query

query: Query = (
    Query(Collection.XXX)
    .yyy()
    .join(
        Join(Collection.WEAPON_DATASHEET)
        .outer(0)
        .on("item_id")
        .to("item_id")
        .inject_at("weapon_datasheet")
    )
)
```

### Deeply nested join

Deeply nested join are necessary in order to access data structures deeper in the collections tree.
To deeply nest joins, instantiate the `Join` class multiple times and combine them through
`join1.nest(join2.nest(join3))` where `join3` is nested within `join2` and `join2` is nested within `join1`:
```
from ps2_census import Collection, Join, Query

item_to_weapon_join: Join = (
    Join(Collection.ITEM_TO_WEAPON)
    .on("item_id")
    .to("item_id")
    .inject_at("item_to_weapon")
)

weapon_join: Join = (
    Join(Collection.WEAPON)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon")
)

weapon_to_fire_group_join: Join = (
    Join(Collection.WEAPON_TO_FIRE_GROUP)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon_to_fire_group")
)

query: Query = (
    Query(Collection.ITEM)
    .filter("item_type_id", ItemType.WEAPON)
    .join(
        item_to_weapon_join.nest(
            weapon_join.nest(
                weapon_to_fire_group_join
            )
        )
    )
)
```

For a deep join you might find it easier to first create the `Join` instances then nest them
as shown above without having too much indentation depth.


### Lateraly nested join

Lateraly nested joins are necessary in order to join between multiple collections at the same depth
in the collections tree.
To lateraly nest joins, instantiate the `Join` class multiple times and combine them through
`join1.nest(join2).nest(join3)` where `join2` and `join3` are nested within `join1`:

```
from ps2_census import Collection, Join, Query

parent_join: Join = (
    Join(Collection.PARENT)
)

child_1_join: Join (
    Join(Collection.CHILD_1)
)

child_2_join: Join (
    Join(Collection.CHILD_1)
)

query: Query = (
    Query(Collection.COLLECTION)
    .join(
        parent_join
        .nest(child_1_join)
        .nest(child_2_join)
    )
)
```

### Tree

Trees are also built using their own class, `Tree`, then passed to the `Query` object:
```
from ps2_census import Collection, Query, Tree

query: Query = (
    Query(Collection.ITEM)
    .tree(
        Tree("name.en")
        .prefix("en_name_")
    )
)
```

## Common enums

Census API data uses a lot of integer enumerations that are collections themselves.

For example the `faction_id` key in items from `Collection.ITEM` is an integer that represents
a specific fation, refering to `Collection.FACTION`: Vanu is `1`, NC is `2` etc.

In order to reduce the amount of necessary joins, which are arguably the most complex part of Census queries,
some common enumerations are provided in `ps2_census.enums` as Python enum.IntEnum classes, including:
- ArmorFacing
- FacilityType
- Faction
- FireModeType
- ItemType
- ItemCategory
- MetagameEventState
- PlayerState
- ProjectileFlightType
- ResistType
- ResourceType
- RewardType
- TargetType
- Vehicle
- World

These typically do not change often and ps2-census will be updated whenever there is such a change.

They can be used just for reference, but also in queries for filtering.

See the following example for filtering weapon items only using `ps2_census.enums.ItemType`:
```
from ps2_census.enums import ItemType
query = (
    Query(Collection.ITEM, service_id=YOUR_SERVICE_ID)
    .filter("item_type_id", ItemType.WEAPON)
)
```

## Event Stream

ps2-census offers a client that handles connection to the WebSocket endpoint, subscription
to various streams and reception of the events.

*Note*: because the client uses the [websockets](https://github.com/aaugustin/websockets) library,
we need to handle async calls.

### Usage

`from ps2_census import EventStream`

First you need to connect to the WebSocket endpoint; to do this, instantiate the `EventStream` class:
```
stream: EventStream = await EventStream(service_id=YOUR_SERVICE_ID)
```

Then, subscribe to events:
```
from ps2_census import CharacterEvent, WorldEvent, EventStreamWorld

await stream.subscribe(
    worlds=[EventStreamWorld.XXX, EventStreamWorld.YYY],
    events=[WorldEvent.ZZZ, CharacterEvent.AAA],
    characters=["1234", "5678"],
    logical_and_characters_with_worlds=True
)
```
Where:
- `worlds` is a list of `EventStreamWorld` objects. Use `[EventStreamWorld.ALL]` for all worlds
- `events` is a list of `CharacterEvent`, `WorldEvent` or `GenericEvent` objects. Use `GenericEvent.ALL` to get all events (character and world)
- `characters` is a list of character IDs as strings
- `logical_and_characters_with_worlds` is True if you want to match all events concerning the characters *AND* the worlds; default is False, so it matches all events concerning the characters *OR* the worlds

You can perform multiple subscriptions one after another on the same `EventStream` object; they are additively merged.

Finally, you need to handle received events from your subscription, for example:
```
while True:
    print(await stream.receive())
```

More information about the Planetside2 Census event stream can be found at [here](http://census.daybreakgames.com/#what-is-websocket).

### Full example
```
from ps2_census import EventStream, CharacterEvent, WorldEvent, EventStreamWorld

stream = await EventStream(service_id=xxx)

await stream.subscribe(worlds=[EventStreamWorld.SOLTECH], events=[WorldEvent.CONTINENT_LOCK, WorldEvent.CONTINENT_UNLOCK])

while True:
    print(await stream.receive())
```

## Development

In order to work on ps2-analysis:
- Setup a virtual environment with python 3.8
- Install [poetry](https://github.com/python-poetry/poetry)
- Install dependencies with `poetry install`
- Run tests with `pytest`
- Update dependencies with `poetry update`
