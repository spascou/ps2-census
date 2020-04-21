from ps2_census import Tree


def test_tree():
    tree = Tree("field_name")
    assert str(tree) == "field:field_name"


def test_list():
    tree = Tree("field_name").list(1)
    assert str(tree) == "field:field_name^list:1"


def test_prefix():
    tree = Tree("field_name").prefix("some_prefix_")
    assert str(tree) == "field:field_name^prefix:some_prefix_"


def test_start():
    tree = Tree("field_name").start("some_node")
    assert str(tree) == "field:field_name^start:some_node"


def test_list_prefix():
    tree = Tree("field_name").list(1).prefix("some_prefix_")
    assert str(tree) == "field:field_name^list:1^prefix:some_prefix_"
