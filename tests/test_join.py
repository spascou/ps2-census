from ps2_census import Collection, Join


def test_join():
    join = Join(Collection.ABILITY)
    assert str(join) == "ability"


def test_on_to():
    join = Join(Collection.ABILITY).on("on_field").to("to_field")
    assert str(join) == "ability^on:on_field^to:to_field"


def test_list():
    join = Join(Collection.ABILITY).list(1)
    assert str(join) == "ability^list:1"


def test_show():
    join = Join(Collection.ABILITY).show("field1", "field2")
    assert str(join) == "ability^show:field1'field2"


def test_hide():
    join = Join(Collection.ABILITY).hide("field1", "field2")
    assert str(join) == "ability^hide:field1'field2"


def test_inject_at():
    join = Join(Collection.ABILITY).inject_at("field")
    assert str(join) == "ability^inject_at:field"


def test_terms():
    join = Join(Collection.ABILITY).terms(field1="value1", field2=2)
    assert str(join) == "ability^terms:field1=value1'field2=2"


def test_outer():
    join = Join(Collection.ABILITY).outer(1)
    assert str(join) == "ability^outer:1"


def test_simple_nest():
    join = Join(Collection.ABILITY).nest(Join(Collection.ACHIEVEMENT))
    assert str(join) == "ability(achievement)"


def test_deep_nest():
    join = Join(Collection.ABILITY).nest(
        Join(Collection.ACHIEVEMENT).nest(Join(Collection.CURRENCY))
    )
    assert str(join) == "ability(achievement(currency))"


def test_lateral_nest():
    join = (
        Join(Collection.ABILITY)
        .nest(Join(Collection.ACHIEVEMENT))
        .nest(Join(Collection.CURRENCY))
    )
    assert str(join) == "ability(achievement,currency)"


def test_items_simple_nest():
    join = (
        Join(Collection.ABILITY)
        .on("parent")
        .nest(Join(Collection.ACHIEVEMENT).on("child"))
    )
    assert str(join) == "ability^on:parent(achievement^on:child)"


def test_items_deep_nest():
    join = (
        Join(Collection.ABILITY)
        .on("parent")
        .nest(
            Join(Collection.ACHIEVEMENT)
            .on("child")
            .nest(Join(Collection.CURRENCY).on("grandchild"))
        )
    )
    assert (
        str(join) == "ability^on:parent(achievement^on:child(currency^on:grandchild))"
    )


def test_items_lateral_nest():
    join = (
        Join(Collection.ABILITY)
        .on("parent")
        .nest(Join(Collection.ACHIEVEMENT).on("child"))
        .nest(Join(Collection.CURRENCY).on("sibling"))
    )
    assert str(join) == "ability^on:parent(achievement^on:child,currency^on:sibling)"
