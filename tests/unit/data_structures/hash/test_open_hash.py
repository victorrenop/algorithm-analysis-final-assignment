from algorithm_analysis_final_assignment.data_structures.hash import OpenHash
from algorithm_analysis_final_assignment.data_structures import Item
import pytest


class TestOpenHash:
    @pytest.mark.parametrize("hash_function", [("linear")])
    def test_insert(self, hash_function):
        # prepare
        hash_map = OpenHash(hash_map_size=11, hash_function_selector=hash_function)
        items_to_insert = [10, 22, 31, 4, 15, 28, 17, 88, 59]
        expected_hash_map = [
            Item(22, 1),
            Item(88, 1),
            None,
            None,
            Item(4, 1),
            Item(15, 1),
            Item(28, 1),
            Item(17, 1),
            Item(59, 1),
            Item(31, 1),
            Item(10, 1),
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
            ("linear", 22, Item(22, 1)),
            ("linear", 17, Item(17, 1)),
        ],
    )
    def test_search(self, hash_function, key, expected_result):
        # prepare
        hash_map = OpenHash(hash_map_size=11, hash_function_selector=hash_function)
        items_to_insert = [10, 22, 31, 4, 15, 28, 17, 88, 59]

        # act
        for item in items_to_insert:
            hash_map.insert(key=item, val=1)
        actual_result = hash_map.search(key)

        # assert
        assert actual_result == expected_result

    def test_hash_function_not_implemented(self):
        # prepare
        hash_map = OpenHash(hash_map_size=1, hash_function_selector="not_implemented")

        # act, assert
        with pytest.raises(NotImplementedError):
            hash_map.insert(1, 1)
