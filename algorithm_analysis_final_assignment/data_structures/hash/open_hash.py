from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.item import Item
from typing import Generator
import dataclasses


class OpenHash(Hash):
    def __init__(self, hash_map_size: int, hash_function_selector: str):
        self.hash_map_size = hash_map_size
        self.hash_map = [None] * hash_map_size
        self.hash_function_selector = hash_function_selector
        self.keys = []

    def insert(self, key: object, val: int) -> None:
        idx = 0
        idx_to_insert = self.hash_function(key, idx)
        while idx < self.hash_map_size and self.hash_map[idx_to_insert] is not None:
            idx += 1
            idx_to_insert = self.hash_function(key, idx)
        if idx < self.hash_map_size:
            self.hash_map[idx_to_insert] = Item(key, val)
            self.keys.append(idx_to_insert)
            return idx_to_insert
        return -1

    def search(self, key: int) -> Item:
        idx = 0
        idx_to_search = self.hash_function(key, idx)
        while (
            idx < self.hash_map_size
            and self.hash_map[idx_to_search] is not None
            and self.hash_map[idx_to_search].key != key
        ):
            idx += 1
            idx_to_search = self.hash_function(key, idx)
        if idx < self.hash_map_size:
            return self.hash_map[idx_to_search]
        return None

    def traverse_keys(self) -> Generator[Item, None, None]:
        for address in self.keys:
            yield dataclasses.replace(self.hash_map[address])

    def hash_function(self, key: int, idx: int) -> int:
        key = self._convert_key(key)
        if self.hash_function_selector == "linear":
            return ((key % self.hash_map_size) + idx) % self.hash_map_size
        elif self.hash_function_selector == "quadratic":
            return (
                (key % self.hash_map_size) + idx + 3 * idx ** 2
            ) % self.hash_map_size
        elif self.hash_function_selector == "double":
            return (
                (key % self.hash_map_size) + idx * (1 + (key % self.hash_map_size - 1))
            ) % self.hash_map_size
        raise NotImplementedError("Hash function not implemented!")
