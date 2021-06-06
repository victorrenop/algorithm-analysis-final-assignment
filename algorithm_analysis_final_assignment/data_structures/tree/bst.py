from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree
from algorithm_analysis_final_assignment.data_structures.item import Item
from dataclasses import dataclass


@dataclass
class BSTNode:
    item: Item
    left: object
    right: object


class BinarySearchTree(Tree):
    def __init__(self):
        self.root = None

    def insert(self, key: object, val: int, current_root: BSTNode = None) -> None:
        if current_root is not None:
            if val > current_root.item.val:
                current_root.right = self.insert(key, val, current_root.right)
            else:
                current_root.left = self.insert(key, val, current_root.left)
        else:
            return BSTNode(left=None, right=None, item=Item(key=key, val=val))
        return current_root

    def search_key(self, key: object, current_root: BSTNode = None) -> BSTNode:
        if current_root is not None:
            if key == current_root.item.key:
                yield current_root.item
            yield from self.search_key(key, current_root.left)
            yield from self.search_key(key, current_root.right)

    def search_val(self, val: int, current_root: BSTNode = None) -> BSTNode:
        if current_root is None:
            yield None
        elif val > current_root.item.val:
            yield from self.search_val(val, current_root.right)
        elif val < current_root.item.val:
            yield from self.search_val(val, current_root.left)
        yield current_root.item

    def get_height(self, node: BSTNode) -> int:
        if node is None:
            return -1
        left_depth = self.get_height(node.left)
        right_depth = self.get_height(node.right)

        if left_depth > right_depth:
            return left_depth + 1
        return right_depth + 1

    def traverse_in_order(self, current_root: BSTNode = None) -> None:
        if current_root is not None:
            yield from self.traverse_in_order(current_root.left)
            yield current_root.item
            yield from self.traverse_in_order(current_root.right)

    def traverse_pre_order(self, current_root: BSTNode = None) -> None:
        if current_root is not None:
            yield current_root.item
            yield from self.traverse_pre_order(current_root.left)
            yield from self.traverse_pre_order(current_root.right)

    def traverse_post_order(self, current_root: BSTNode = None) -> None:
        if current_root is not None:
            yield from self.traverse_pre_order(current_root.left)
            yield from self.traverse_pre_order(current_root.right)
            yield current_root.item
