from algorithm_analysis_final_assignment.data_structures.tree import BinarySearchTree
from algorithm_analysis_final_assignment.data_structures import Item
import pytest


class TestBinarySearchTree:
    def prepare_tree(self):
        return BinarySearchTree(), [15, 7, 25, 5, 10, 3, 4]

    def test_insert(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)

        # assert
        assert tree.root.item.val == 15
        assert tree.root.right.item.val == 25
        assert tree.root.left.item.val == 7
        assert tree.root.left.left.item.val == 5
        assert tree.root.left.right.item.val == 10
        assert tree.root.left.left.left.item.val == 3
        assert tree.root.left.left.left.right.item.val == 4

    @pytest.mark.parametrize(
        "key,expected_item",
        [
            (5, Item(key=5, val=3)),
            (0, Item(key=0, val=15)),
            (2, Item(key=2, val=25)),
        ],
    )
    def test_search_key(self, key, expected_item):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_item = next(tree.search_key(key, tree.root), None)

        # assert
        assert actual_item == expected_item

    @pytest.mark.parametrize(
        "val,expected_item",
        [
            (15, Item(key=0, val=15)),
            (3, Item(key=5, val=3)),
            (25, Item(key=2, val=25)),
        ],
    )
    def test_search_val(self, val, expected_item):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_item = next(tree.search_val(val, tree.root), None)

        # assert
        assert actual_item == expected_item

    def test_get_height(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()
        expected_height = 4

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_height = tree.get_height(tree.root)

        # assert
        assert actual_height == expected_height

    def test_traverse_in_order(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()
        expected_nodes = sorted(
            [Item(key=idx, val=val) for idx, val in enumerate(nodes_to_insert)],
            key=lambda x: x.val,
        )

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_nodes = list(tree.traverse_in_order(tree.root))

        # assert
        assert actual_nodes == expected_nodes

    def test_traverse_pre_order(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()
        expected_nodes = [
            Item(key=0, val=15),
            Item(key=1, val=7),
            Item(key=3, val=5),
            Item(key=5, val=3),
            Item(key=6, val=4),
            Item(key=4, val=10),
            Item(key=2, val=25),
        ]

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_nodes = list(tree.traverse_pre_order(tree.root))

        # assert
        assert actual_nodes == expected_nodes

    def test_traverse_post_order(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()
        expected_nodes = [
            Item(key=1, val=7),
            Item(key=3, val=5),
            Item(key=5, val=3),
            Item(key=6, val=4),
            Item(key=4, val=10),
            Item(key=2, val=25),
            Item(key=0, val=15),
        ]

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_nodes = list(tree.traverse_post_order(tree.root))

        # assert
        assert actual_nodes == expected_nodes
