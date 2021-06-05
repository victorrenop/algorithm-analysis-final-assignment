from abc import ABCMeta, abstractmethod


class Tree(metaclass=ABCMeta):
    @abstractmethod
    def insert(self, key: object, val: int, current_root: object = None) -> None:
        pass

    @abstractmethod
    def search_key(self, key: object) -> object:
        pass

    @abstractmethod
    def search_val(self, val: int) -> object:
        pass

    @abstractmethod
    def get_height(self, current_root: object) -> int:
        pass

    @abstractmethod
    def traverse_in_order(self, current_root: object) -> None:
        pass

    @abstractmethod
    def traverse_pre_order(self, current_root: object) -> None:
        pass

    @abstractmethod
    def traverse_post_order(self, current_root: object) -> None:
        pass
