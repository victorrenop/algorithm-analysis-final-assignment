[924, 220, 911, 244, 898, 258, 362, 363, 360, 350]
from algorithm_analysis_final_assignment.data_structures.tree import AVLTree
from algorithm_analysis_final_assignment.data_structures.tree import Item
import pytest


class TestAVLTree:
    def prepare_tree(self):
        return AVLTree(), [924, 220, 911, 244, 898, 258, 362, 363, 360, 350]

    def test_insert(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)

        # assert
        assert tree.root.item.val == 362
        assert tree.root.left.item.val == 258
        assert tree.root.left.left.item.val == 244
        assert tree.root.left.left.left.item.val == 220
        assert tree.root.left.right.item.val == 360
        assert tree.root.left.right.left.item.val == 350
        assert tree.root.right.item.val == 898
        assert tree.root.right.left.item.val == 363
        assert tree.root.right.right.item.val == 911
        assert tree.root.right.right.right.item.val == 924

    @pytest.mark.parametrize(
        "key,expected_item",
        [
            (6, Item(key=6, val=362)),
            (1, Item(key=1, val=220)),
            (0, Item(key=0, val=924)),
            (9, Item(key=9, val=350)),
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
            (362, Item(key=6, val=362)),
            (220, Item(key=1, val=220)),
            (924, Item(key=0, val=924)),
            (350, Item(key=9, val=350)),
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
        expected_height = 3

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
        [924, 220, 911, 244, 898, 258, 362, 363, 360, 350]
        expected_nodes = [
            Item(key=6, val=362),
            Item(key=5, val=258),
            Item(key=3, val=244),
            Item(key=1, val=220),
            Item(key=8, val=360),
            Item(key=9, val=350),
            Item(key=4, val=898),
            Item(key=7, val=363),
            Item(key=2, val=911),
            Item(key=0, val=924),
        ]

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_nodes = list(tree.traverse_pre_order(tree.root))
        print(actual_nodes)

        # assert
        assert actual_nodes == expected_nodes

    def test_traverse_post_order(self):
        # prepare
        tree, nodes_to_insert = self.prepare_tree()
        expected_nodes = [
            Item(key=5, val=258),
            Item(key=3, val=244),
            Item(key=1, val=220),
            Item(key=8, val=360),
            Item(key=9, val=350),
            Item(key=4, val=898),
            Item(key=7, val=363),
            Item(key=2, val=911),
            Item(key=0, val=924),
            Item(key=6, val=362),
        ]

        # act
        for idx, node in enumerate(nodes_to_insert):
            tree.root = tree.insert(key=idx, val=node, current_root=tree.root)
        actual_nodes = list(tree.traverse_post_order(tree.root))

        # assert
        assert actual_nodes == expected_nodes
