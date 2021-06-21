from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.item import Item
from typing import Generator
import dataclasses
from math import floor


class LinkedHash(Hash):
    def __init__(self, hash_map_size: int, hash_function_selector: str):
        self.hash_map_size = hash_map_size
        self.hash_map = [None] * hash_map_size
        self.hash_function_selector = hash_function_selector
        self.keys = []

    def insert(self, key: object, val: int) -> int:
        idx_to_insert = self.hash_function(key)
        if self.hash_map[idx_to_insert] is None:
            self.hash_map[idx_to_insert] = []
        self.hash_map[idx_to_insert].append(Item(key, val))
        self.keys.append((idx_to_insert, len(self.hash_map[idx_to_insert]) - 1))

        return idx_to_insert

    def search(self, key: int) -> Item:
        idx_to_search = self.hash_function(key)
        if self.hash_map[idx_to_search] is not None:
            for item in self.hash_map[idx_to_search]:
                if key == item.key:
                    return item
        return None

    def traverse_keys(self) -> Generator[Item, None, None]:
        for address in self.keys:
            yield dataclasses.replace(self.hash_map[address[0]][address[1]])

    def hash_function(self, key: object) -> int:
        key = self._convert_key(key)
        if self.hash_function_selector == "division":
            return key % self.hash_map_size
        elif self.hash_function_selector == "multiplication":
            return int(floor(self.hash_map_size * (key * 0.618 % 1)))
        raise NotImplementedError("Hash function not implemented!")
