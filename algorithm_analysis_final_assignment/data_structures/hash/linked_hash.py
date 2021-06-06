from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.item import Item


class LinkedHash(Hash):
    def __init__(self, hash_map_size: int, hash_function_selector: str):
        self.hash_map_size = hash_map_size
        self.hash_map = [None] * hash_map_size
        self.hash_function_selector = hash_function_selector

    def insert(self, key: object, val: int) -> int:
        idx_to_insert = self.hash_function(key)
        if self.hash_map[idx_to_insert] is None:
            self.hash_map[idx_to_insert] = []
        self.hash_map[idx_to_insert].append(Item(key, val))

        return idx_to_insert

    def search(self, key: int) -> Item:
        idx_to_search = self.hash_function(key)
        if self.hash_map[idx_to_search] is not None:
            for item in self.hash_map[idx_to_search]:
                if key == item.key:
                    return item
        return None

    def hash_function(self, key: object) -> int:
        if self.hash_function_selector == "division":
            return key % self.hash_map_size
        raise NotImplementedError("Hash function not implemented!")
