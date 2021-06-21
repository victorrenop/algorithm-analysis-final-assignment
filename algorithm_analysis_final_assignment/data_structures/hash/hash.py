from abc import ABCMeta, abstractmethod
from typing import Generator
from algorithm_analysis_final_assignment.data_structures import Item


class Hash(metaclass=ABCMeta):
    @abstractmethod
    def insert(self, key: object, val: int) -> int:
        pass

    @abstractmethod
    def search(self, key: object) -> Item:
        pass

    @abstractmethod
    def hash_function(self, key: object) -> int:
        pass

    @abstractmethod
    def traverse_keys(self) -> Generator[Item, None, None]:
        pass

    def update(self, key: object, val: int) -> None:
        item = self.search(key)
        if item:
            item.val = val
        else:
            self.insert(key, val)

    def get(self, key: object, default_return: object = None) -> object:
        search_result = self.search(key)
        return search_result.val if search_result else default_return

    def _convert_key(self, key: object) -> int:
        if isinstance(key, str):
            return sum(ord(char) for char in key)
        return int(key)

    def __setitem__(self, key: object, item: object) -> None:
        self.update(key, item)

    def __getitem__(self, key: object) -> object:
        return self.search(key).val
