from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.item import Item


class OpenHash(Hash):
    def __init__(self, hash_map_size: int, hash_function_selector: str):
        self.hash_map_size = hash_map_size
        self.hash_map = [None] * hash_map_size
        self.hash_function_selector = hash_function_selector

    def insert(self, key: object, val: int) -> None:
        idx = 0
        idx_to_insert = self.hash_function(key, idx)
        while idx < self.hash_map_size and self.hash_map[idx_to_insert] is not None:
            idx += 1
            idx_to_insert = self.hash_function(key, idx)
        if idx < self.hash_map_size:
            self.hash_map[idx_to_insert] = Item(key, val)
            return idx_to_insert
        return -1

    def search(self, key: int) -> Item:
        idx = 0
        idx_to_search = self.hash_function(key, idx)
        while idx < self.hash_map_size and self.hash_map[idx_to_search].key != key:
            idx += 1
            idx_to_search = self.hash_function(key, idx)
        if idx < self.hash_map_size:
            return self.hash_map[idx_to_search]
        return None

    def hash_function(self, key: int, idx: int) -> int:
        if self.hash_function_selector == "linear":
            return ((key % self.hash_map_size) + idx) % self.hash_map_size
        raise NotImplementedError("Hash function not implemented!")
