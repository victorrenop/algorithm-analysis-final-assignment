from abc import ABCMeta, abstractmethod
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
