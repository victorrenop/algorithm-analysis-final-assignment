from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree
from algorithm_analysis_final_assignment.data_structures.item import Item
from dataclasses import dataclass


@dataclass
class AVLNode:
    item: Item
    height: int
    left: object
    right: object


class AVLTree(Tree):
    def __init__(self):
        self.root = None

    def insert(self, key: object, val: int, current_root: AVLNode = None) -> None:
        if current_root != None:
            if val > current_root.item.val:
                current_root.right = self.insert(key, val, current_root.right)
            else:
                current_root.left = self.insert(key, val, current_root.left)
        else:
            return AVLNode(left=None, right=None, item=Item(key=key, val=val), height=1)

        current_root.height = (
            max(
                self._get_node_height(current_root.left),
                self._get_node_height(current_root.right),
            )
            + 1
        )
        balancing_factor = self._get_balancing_factor(current_root)

        if (
            balancing_factor > 1
            and val < current_root.item.val
            and val < current_root.left.item.val
        ):
            return self._simple_right_rotation(current_root)
        if (
            balancing_factor > 1
            and val > current_root.item.val
            and val > current_root.right.item.val
        ):
            return self._simple_left_rotation(current_root)
        if (
            balancing_factor > 1
            and val < current_root.item.val
            and val > current_root.left.item.val
        ):
            current_root.left = self._simple_left_rotation(current_root.left)
            return self._simple_right_rotation(current_root)
        if (
            balancing_factor > 1
            and val > current_root.item.val
            and val < current_root.right.item.val
        ):
            current_root.right = self._simple_right_rotation(current_root.right)
            return self._simple_left_rotation(current_root)
        return current_root

    def search_key(self, key: object, current_root: AVLNode = None) -> AVLNode:
        if current_root is not None:
            if key == current_root.item.key:
                yield current_root.item
            yield from self.search_key(key, current_root.left)
            yield from self.search_key(key, current_root.right)

    def search_val(self, val: int, current_root: AVLNode = None) -> AVLNode:
        if current_root is None:
            yield None
        elif val > current_root.item.val:
            yield from self.search_val(val, current_root.right)
        elif val < current_root.item.val:
            yield from self.search_val(val, current_root.left)
        yield current_root.item

    def get_height(self, node: AVLNode) -> int:
        if node is None:
            return -1
        left_depth = self.get_height(node.left)
        right_depth = self.get_height(node.right)

        if left_depth > right_depth:
            return left_depth + 1
        return right_depth + 1

    def _get_node_height(self, node: AVLNode) -> int:
        if node == None:
            return 0
        return node.height

    def _get_balancing_factor(self, node: AVLNode) -> int:
        if node == None:
            return 0
        return abs(self._get_node_height(node.left) - self._get_node_height(node.right))

    def _get_int_balancing_factor(self, node: AVLNode) -> int:
        if node == None:
            return 0
        return self._get_node_height(node.left) - self._get_node_height(node.right)

    def _simple_left_rotation(self, k2: AVLNode) -> AVLNode:
        k1 = k2.right
        k2.right = k1.left
        k1.left = k2

        k2.height = (
            max(self._get_node_height(k2.left), self._get_node_height(k2.right)) + 1
        )
        k1.height = max(self._get_node_height(k1.right), k2.height) + 1

        return k1

    def _simple_right_rotation(self, k2: AVLNode) -> AVLNode:
        k1 = k2.left
        k2.left = k1.right
        k1.right = k2

        k2.height = (
            max(self._get_node_height(k2.left), self._get_node_height(k2.right)) + 1
        )
        k1.height = max(self._get_node_height(k1.left), k2.height) + 1

        return k1

    def traverse_in_order(self, current_root: AVLNode = None) -> None:
        if current_root is not None:
            yield from self.traverse_in_order(current_root.left)
            yield current_root.item
            yield from self.traverse_in_order(current_root.right)

    def traverse_pre_order(self, current_root: AVLNode = None) -> None:
        if current_root is not None:
            yield current_root.item
            yield from self.traverse_pre_order(current_root.left)
            yield from self.traverse_pre_order(current_root.right)

    def traverse_post_order(self, current_root: AVLNode = None) -> None:
        if current_root is not None:
            yield from self.traverse_pre_order(current_root.left)
            yield from self.traverse_pre_order(current_root.right)
            yield current_root.item
