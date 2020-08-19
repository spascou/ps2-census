![coverage-badge](./badges/coverage.svg)

# ps2-census

*ps2-census* is a low-level client for Daybreak's Planetside 2 Census API written in Python >= 3.8.

   * [ps2-census](#ps2-census)
      * [Installation](#installation)
      * [Full examples](#full-examples)
      * [Query building](#query-building)
         * [Basic query](#basic-query)
         * [Simple join](#simple-join)
         * [Nesting joins](#nesting-joins)
            * [Deeply nested join](#deeply-nested-join)
            * [Lateraly nested joins](#lateraly-nested-joins)
         * [Tree](#tree)
      * [Factories](#factories)
      * [Common enums](#common-enums)
      * [Event Stream](#event-stream)
         * [Usage](#usage)
      * [Next steps](#next-steps)
      * [Similar projects](#similar-projects)
      * [Development](#development)
         * [Environment](#environment)
         * [Technical details](#technical-details)

*Features*:
- Build queries through method chaining
- Join collections and nest them through method chaining
- Get raw (deserialized) responses as Python dictionaries
- Access common enums directly
- Subscribe to event streams

By default the `example` service ID is used; however it is not recommended for production.
You should get your own service ID from the webside below and supply it to the client whenever needed.

More information about the Census API is available on the official Census documentation [here](http://census.daybreakgames.com/).

[Iridar's blog](https://iridar-mirror.knyazev.io/index.html%3Fp=4127.html) is also recommended to understand
the quirks of this particular API as this knowledge is necessary to use *ps2-census* properly.

## Installation

```sh
pip install ps2-census
```

## Full examples

Before diving in the details of the *ps2-census* client, full examples are available in the `examples` folder.

They currently include:
- `all_about_trac_5.py` (and the output in `all_about_trac_5.json`): building and executing a query that
fetches pretty much everything that's to know about the TR TRAC-5 carbine
- `character_death_event_stream.py` (and the output in `caracter_death_event_stream.ndjson`): subscribing to
all character death events on the SolTech server, receive at most 20 events and print them, then gracefuly
disconnect

## Query building

Queries are made on collections with optional joins on other collections as well as various
commands that alter the output.

A Census API collection is analog to a relation in a generic relational database system, and a
Census API join is analog to a join between these relations.

### Basic query

To build a query, instantiate the `Query` class with a `Collection` (and your service ID,
though it will be omitted in next examples for conciseness):
```python
from ps2_census import Collection, Query

query: Query = Query(Collection.ITEM, service_id=YOUR_SERVICE_ID)
```

Chain methods to alter the query further:
```python
query: Query = (
    Query(Collection.ITEM)
    .lang("en")
    .sort(("item_id", 1), ("faction_id", -1))
    .limit(30)
    [...]
)
```

Available methods are:
- `filter(field: str, value: Union[str, int], modifier: Optional[SearchModifier])`: filter
the query on a field; `ps2_census.SearchModifier` contains all the modifiers made available
by the Census API (`SearchModifier.CONTAINS`, `SearchModifier.LESS_OR_EQUAL`, ...)
- `show(*args: str)`: only return the provided fields in results
- `hide(*args: str)`: do not return the provided fields in results
- `sort(*args: Tuple[str, Literal[1, -1]])`: sort the results by field, either in increasing or decreasing order
- `has(*args: str)`: only return results which have the specified fields
- `case(arg: bool)`: whether `filter()`s are case sensive or not; default to `True`
- `limit(arg: int)`: limit the return to *at most* `arg` results; required in tendem with `start()` for queries having too large of a result and therefore fail; defaults to `1`
- `limit_per_db(arg: int)`: limit the return to *at most* `arg * databases count` results; useful when
querying the `Collection.CHARACTER` collection whose objects are randomly distributed among multiple
databases in order to have more predictable results
- `start(arg: int)`: start with the `arg`th object within the results of the query
- `include_null(arg: bool)`: whether to include keys with `None` values in results; defaults to `False`
- `lang(arg: str)`: only keep the supplied language for internationalized strings
- `join(arg: Join)`: perform a collection join; see the following documentation for additional details
- `tree(arg: Tree)`: rearrange lists of data into trees; see the following documentation for additional details
- `timing(arg: bool)`: show query timing information
- `exact_match_first(arg: bool)`: when using `filter()`s with `SearchModifier`s, put exact matches at the top of the
results list disregarding `sort()`s
- `distinct(arg: str)`: get the distinct values for a certain field
- `retry(arg: bool)`: retry queries at most one time before failing; defaults to `True`

Execute the query in one of the 2 ways made available by the Census API:

- `.count()` to get the items count
```python
query.count()
> {'count': 21048}
```

- `.get()` to get the results
```python
query.get()
> {'item_list': [{...}, {...}, ...], 'returned': 30}
```

`count()` and `get()` calls are when the query is actually sent to the Census API endpoint.
They will raise status exceptions if appropriate.

### Simple join

In order to perform joins instantiate the `Join` class with a `Collection`, add any additional
chained methods to it, and pass it to the `Query` object via `query.join()`:
```python
from ps2_census import Collection, Join, Query

query: Query = (
    Query(Collection.ITEM)
    .join(
        Join(Collection.WEAPON_DATASHEET)
        .outer(0)
        .on("item_id")
        .to("item_id")
        .inject_at("weapon_datasheet")
        [...]
    )
)
```

Available `Join` methods are:
- `nest(other: Join)`: nest another join within this one; see the following documentation for additional details
- `on(arg: str)`: specify the field on this collection (the `Query` or parent `Join`) to join on; if not provided will default to this collection's ID (`{this_type}_id`)
- `to(arg: str)`: specify the field on the other collection (the `Join`'s) to join to; if not provided will default to the `on` value
- `list(arg: Literal[0, 1])`: whether the joined data is a list (and therefore will result in a list of objects) or not; `1` if it is a list, `0` if not; default to `0`
- `show(*args: str)`: only keep the provided fields in results
- `hide(*args: str)`: do not keep the provided fields in results
- `inject_at(arg: str)`: the field name where the joined data will be injected in the parent element (`Query` result item or parent `Join` element)
- `terms(*args: Tuple[str, Union[str, int]])`: filter the join result by conditions (eg. `terms(("faction_id", 1), ("skill_set_id", 129))`)
- `outer(arg: Literam[0, 1])`: whether the join will perform an outer join (include non-matches) of an inner join (exclude non-matches); `1` for outer, `0` for inner; defaults to `1`

Multiple joins can be performed one after another on the same `Query` and the trees will be merged in
the result:
```python
query: Query = (
    Query(Collection.ITEM)
    .join(
        Join(Collection.WEAPON_DATASHEET)
    )
    .join(
        Join(Collection.ITEM_TO_WEAPON)
    )
)
```
### Nesting joins

`Join`s can be nested one into another both deeply and lateraly. Nesting is done by reference: each `Join` instance
contains a list of references to its nested `Join`s.

*Note*: be careful about modifying the `Join` instances after their creation if you assign them to locals
for convenience, as shown in the following examples.
As nesting is done by reference and the whole structure is "compiled" (into a querystring) on the call
to `query.join()`, if any modification is done to an instance between its creation and the resolution,
it will indirectly impact the result of any other parent and/or nested `Join`.
Make use of the below described factories to make clean copies of your instances as necessary.

#### Deeply nested join

Deeply nested join are necessary in order to access data structures deeper in the collections tree.
To deeply nest joins, instantiate the `Join` class multiple times and combine them through
`join1.nest(join2.nest(join3))` where `join3` is nested within `join2` and `join2` is nested within `join1`:
```python
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

#### Lateraly nested joins

Lateraly nested joins are necessary in order to access data structures at the same depth in the collections tree.
To laterally nest joins, instantiate the `Join` class multiple times and combine them through
`join1.nest(join2).nest(join3)` where `join2` and `join3` are nested within `join1`:

```python
from ps2_census import Collection, Join, Query

fire_group_to_fire_mode_join: Join = (
    Join(Collection.FIRE_GROUP_TO_FIRE_MODE)
    .outer(0)
    .on("fire_group_id")
    .to("fire_group_id")
    .list(1)
    .inject_at("fire_group_to_fire_modes")
)

fire_mode_join: Join = (
    Join(Collection.FIRE_MODE_2)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode")
)

fire_mode_to_projectile_join: Join = (
    Join(Collection.FIRE_MODE_TO_PROJECTILE)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode_to_projectile")
)

player_state_group_join: Join = (
    Join(Collection.PLAYER_STATE_GROUP_2)
    .outer(0)
    .on("player_state_group_id")
    .to("player_state_group_id")
    .list(1)
    .inject_at("player_state_groups")
)

query: Query = (
    Query(Collection.WEAPON_TO_FIRE_GROUP)
    .join(
        fire_group_to_fire_mode_join
        .nest(
            fire_mode_join
            .nest(fire_mode_to_projectile_join)
            .nest(player_state_group_join)
        )
    )
)
```

### Tree

Trees are also built using their own class, `Tree`, then passed to the `Query` object:
```python
from ps2_census import Collection, Query, Tree

query: Query = (
    Query(Collection.ITEM)
    .tree(
        Tree("name.en")
        .prefix("en_name_")
        [...]
    )
)
```

This will return a dictionary of items with their english name prefixed by `en_name_` as keys
and the objects themselves as values, instead of a flat list of items.

Available methods are:
- `list(arg: Literal[0, 1])`: `0` if tree data is not a list, `1` if it is a list; defaults to `0`
- `prefix(arg: str)`: prefix to add to the field value
- `start(arg: str)`: where the tree starts; defaults to the root (root list objects will be formatted as a tree)

## Factories

In order to ease the project-wide definition of `Query`, `Join` and `Tree` objects,
each of these classes has a `get_factory()` method.

Upon invocation it saves a copy of the current object and returns a callable that, upon each invocation,
returns a fresh copy of that saved state.

```python
query: Query = Query(Collection.ABILITY).has("someField").case(False)

query_factory: Callable[[], Query] = query.get_factory()

query_copy: Query = query_factory()

assert query == query_copy
> True

query = query.timing(True)

assert query != query_copy
> True

query_copy = query_copy.lang("en")

another_copy = query_factory()

assert query == another_copy
> True

assert query_copy != another_copy
> True
```

Factories obtained in this way are useful to define `Query`, `Join` or `Tree`s somewhere in your code and store
their factory callables, with the guarantee that you cannot modify the shared definition anywhere.

*my_module.py*
```python
from ps2_census import Query, Collection

my_query_factory: Callable[[], Query] = (
    Query(Collection.ABILITY)
    .lang("en")
    .get_factory()
)
```

*main.py*
```python
from my_module import my_query_factory

query: Query = my_query_factory()
query.start(100)  # does not modify any shared object
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

These typically do not change often and *ps2-census* will be updated whenever there is such a change.

They can be used just for reference, but also in queries for filtering.

See the following example for filtering weapon items only using `ps2_census.enums.ItemType`:
```python
from ps2_census.enums import ItemType
query = (
    Query(Collection.ITEM)
    .filter("item_type_id", ItemType.WEAPON)
)
```

## Event Stream

*ps2-census* offers a client that handles connection to the WebSocket endpoint, subscription
to various streams and reception of the events.

*Note*: because the client uses the [websockets](https://github.com/aaugustin/websockets) library,
we need to handle async calls.

### Usage


First you need to connect to the WebSocket endpoint; to do this, instantiate the `EventStream` class:
```python
from ps2_census import EventStream

stream: EventStream = await EventStream(service_id=YOUR_SERVICE_ID)
```

Then, subscribe to events:
```python
from ps2_census import CharacterEvent, WorldEvent, EventStreamWorld, GenericCharacter

await stream.subscribe(
    worlds=[EventStreamWorld.SOLTECH, EventStreamWorld.BRIGGS],
    events=[CharacterEvent.DEATH, WorldEvent.CONTINENT_LOCK],
    characters=[GenericCharacter.ALL, "1234", "5678"],
    logical_and_characters_with_worlds=True
)
```
Where:
- `worlds` is a list of `EventStreamWorld` objects. Use `[EventStreamWorld.ALL]` for all worlds
- `events` is a list of `CharacterEvent`, `WorldEvent` or `GenericEvent` objects. Use `GenericEvent.ALL` to get all events (character and world)
- `characters` is a list of character IDs as strings or the special `GenericCharacter.ALL` to subscribe to all characters
- `logical_and_characters_with_worlds` is True if you want to match all events concerning the characters *AND* the worlds; default is False, so it matches all events concerning the characters *OR* the worlds

You can perform multiple subscriptions one after another on the same `EventStream` object; they are additively merged.

Finally, you need to handle received events from your subscription:
```python
await stream.receive()
```

This simple example put together (you might want to develop it further to do more than simply print events,
handle graceful deconnection, etc):

```python
import asyncio

from ps2_census import CharacterEvent, WorldEvent, EventStream, EventStreamWorld, GenericCharacter

async def main():
    stream: EventStream = await EventStream()

    await stream.subscribe(
        worlds=[EventStreamWorld.SOLTECH, EventStreamWorld.BRIGGS],
        events=[CharacterEvent.DEATH, WorldEvent.CONTINENT_LOCK],
        characters=[GenericCharacter.ALL, "1234", "5678"],
        logical_and_characters_with_worlds=True
    )

    while True:
        print(await stream.receive())

asyncio.run(main())
```

More information about the Planetside2 Census event stream can be found at [here](http://census.daybreakgames.com/#what-is-websocket).

## Next steps

- Improve the `EventStream` client to make it slightly higher-level (handle disconnections,
filter events, etc)

## Similar projects

- *leonhard-s*' [auraxium](https://github.com/leonhard-s/auraxium)

## Development

### Environment

In order to develop *ps2-census*:
- Setup a virtual environment with python 3.8
- Install [poetry](https://github.com/python-poetry/poetry)
- Install dependencies with `poetry install`
- Run tests with `pytest`
- Update dependencies with `poetry update`

### Technical details

All interaction with the Census API (except the WebSocket events stream part) is done through
query parameters. Query bodies are always empty and all information is carried in the query URL string.

*ps2-census*' objective is to wrap the building of these (often very long and complex)
querystrings and provide a comfortable, structured programmatic interface.

To achieve that, we make use of the `Query` class which:
- on initialization sets up basic query elements such as endpoint, service ID, collection and namespace,
- at each "command" method call adds query parameters to its `parameters` dictionary attribute,
- at `get()` or `count()` build the actual URL and execute the query using the `requests` library.

Collection joins are more complicated as they are not built as proper query parameters;
inside the final query, each call to `query.join()` creates a new query parameter, eg.
`...&c:join={join_string}&...` with the `join_string` being written in a specific format.

Hence the `Join` class which:
- on initialization sets up the collection,
- at each method call adds items to its `items` dictionary attribute,
- at each `nest()` call stores a reference to the nested `Join` instance in its `nested_joins` list attribute,
- at `__str__()` builds the `join_string` that will become a main query's parameter value, in the specific format
and using the `items` elements as well as recursively calling `__str__()` on `nested_joins` items.

Therefore, the `join_string` is not actually computed before a call to a `Join` instance's `__str__()` method,
and it is recursively computed across nested joins.

The event streams part is more conventional, as *ps2-census* just needs to connect to a WebSocket endpoint, issue
subscription commands in a custom but simple format and then read messages from the stream.
