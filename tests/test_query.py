from ps2_census import Collection, Join, Namespace, Query, SearchModifier, Tree
from ps2_census.constants import Verb


def test_query():
    query = Query(
        Collection.ABILITY,
        endpoint="someendpoint",
        service_id="someserviceid",
        namespace=Namespace.PS2_V2,
    )

    assert query._get_url(Verb.GET) == "someendpoint/s:someserviceid/get/ps2:v2/ability"
    assert (
        query._get_url(Verb.COUNT)
        == "someendpoint/s:someserviceid/count/ps2:v2/ability"
    )


def test_filter():
    query = (
        Query(Collection.ABILITY)
        .filter("fieldname", "fieldvalue")
        .filter("anotherfieldname", "anotherfieldvalue", SearchModifier.STARTS_WITH)
    )

    assert query.parameters == {
        "fieldname": "fieldvalue",
        "anotherfieldname": "^anotherfieldvalue",
    }


def test_show():
    query = Query(Collection.ABILITY).show("field1", "field2")

    assert query.parameters == {
        "c:show": "field1,field2",
    }


def test_hide():
    query = Query(Collection.ABILITY).hide("field1", "field2")

    assert query.parameters == {
        "c:hide": "field1,field2",
    }


def test_sort():
    query = Query(Collection.ABILITY).sort(
        ("field1", None), ("field2", 1), ("field3", -1)
    )

    assert query.parameters == {
        "c:sort": "field1,field2:1,field3:-1",
    }


def test_has():
    query = Query(Collection.ABILITY).has("field1", "field2")

    assert query.parameters == {
        "c:has": "field1,field2",
    }


def test_case():
    query_t = Query(Collection.ABILITY).case(True)
    query_f = Query(Collection.ABILITY).case(False)

    assert query_t.parameters == {
        "c:case": "true",
    }
    assert query_f.parameters == {
        "c:case": "false",
    }


def test_limit():
    query = Query(Collection.ABILITY).limit(100)

    assert query.parameters == {"c:limit": "100"}


def test_limit_per_db():
    query = Query(Collection.ABILITY).limit_per_db(100)

    assert query.parameters == {"c:limitPerDB": "100"}


def test_start():
    query = Query(Collection.ABILITY).start(100)

    assert query.parameters == {"c:start": "100"}


def test_include_null():
    query_t = Query(Collection.ABILITY).include_null(True)
    query_f = Query(Collection.ABILITY).include_null(False)

    assert query_t.parameters == {
        "c:includeNull": "true",
    }
    assert query_f.parameters == {
        "c:includeNull": "false",
    }


def test_lang():
    query = Query(Collection.ABILITY).lang("en")

    assert query.parameters == {
        "c:lang": "en",
    }


def test_join():
    join = Join(Collection.ACHIEVEMENT)
    query = Query(Collection.ABILITY).join(join)

    assert query.parameters == {"c:join": str(join)}


def test_tree():
    tree = Tree("somefield")
    query = Query(Collection.ABILITY).tree(tree)

    assert query.parameters == {"c:tree": str(tree)}


def test_timing():
    query_t = Query(Collection.ABILITY).timing(True)
    query_f = Query(Collection.ABILITY).timing(False)

    assert query_t.parameters == {
        "c:timing": "true",
    }
    assert query_f.parameters == {
        "c:timing": "false",
    }


def test_exact_match_first():
    query_t = Query(Collection.ABILITY).exact_match_first(True)
    query_f = Query(Collection.ABILITY).exact_match_first(False)

    assert query_t.parameters == {
        "c:exactMatchFirst": "true",
    }
    assert query_f.parameters == {
        "c:exactMatchFirst": "false",
    }


def test_distinct():
    query = Query(Collection.ABILITY).distinct("somefield")

    assert query.parameters == {"c:distinct": "somefield"}


def test_retry():
    query_t = Query(Collection.ABILITY).retry(True)
    query_f = Query(Collection.ABILITY).retry(False)

    assert query_t.parameters == {
        "c:retry": "true",
    }
    assert query_f.parameters == {
        "c:retry": "false",
    }
