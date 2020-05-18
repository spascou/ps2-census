from typing import Callable

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


def test_equality():
    tree1 = Tree("field_name").start("some_node")
    tree2 = Tree("field_name").start("some_node")

    assert tree1 == tree2

    tree1 = tree1.list(1)

    assert tree1 != tree2

    assert tree1 != object()


def test_factory():
    tree: Tree = Tree("field_name").start("node")

    factory: Callable[[], Tree] = tree.get_factory()
    new_tree: Tree = factory()

    assert new_tree == tree

    tree = tree.list(1)

    assert new_tree != tree


def test_factory_alteration():
    tree: Tree = Tree("field_name").start("node")

    factory: Callable[[], Tree] = tree.get_factory()
    new_tree: Tree = factory()

    assert new_tree == tree

    new_tree = new_tree.list(1)
    new_new_tree: Tree = factory()

    assert new_new_tree == tree
