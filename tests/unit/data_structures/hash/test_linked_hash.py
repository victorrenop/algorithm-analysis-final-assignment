from algorithm_analysis_final_assignment.data_structures.hash import LinkedHash
from algorithm_analysis_final_assignment.data_structures import Item
import pytest


class TestLinkedHash:
    @pytest.mark.parametrize("hash_function", [("division")])
    def test_insert(self, hash_function):
        # prepare
        hash_map = LinkedHash(hash_map_size=9, hash_function_selector=hash_function)
        items_to_insert = [5, 28, 19, 15, 20, 33, 12, 17, 10]
        expected_hash_map = [
            None,
            [Item(28, 1), Item(19, 1), Item(10, 1)],
            [Item(20, 1)],
            [Item(12, 1)],
            None,
            [Item(5, 1)],
            [Item(15, 1), Item(33, 1)],
            None,
            [Item(17, 1)],
        ]

        # act
        for item in items_to_insert:
            hash_map.insert(key=item, val=1)
        actual_hash_map = hash_map.hash_map

        # assert
        assert actual_hash_map == expected_hash_map

    @pytest.mark.parametrize(
        "hash_function,key,expected_result",
        [
            ("division", 33, Item(33, 1)),
            ("division", 5, Item(5, 1)),
            ("division", 999, None),
        ],
    )
    def test_search(self, hash_function, key, expected_result):
        # prepare
        hash_map = LinkedHash(hash_map_size=9, hash_function_selector=hash_function)
        items_to_insert = [5, 28, 19, 15, 20, 33, 12, 17, 10]

        # act
        for item in items_to_insert:
            hash_map.insert(key=item, val=1)
        actual_result = hash_map.search(key)

        # assert
        assert actual_result == expected_result

    def test_hash_function_not_implemented(self):
        # prepare
        hash_map = LinkedHash(hash_map_size=1, hash_function_selector="not_implemented")

        # act, assert
        with pytest.raises(NotImplementedError):
            hash_map.insert(1, 1)
