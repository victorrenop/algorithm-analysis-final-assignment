from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree
from typing import Generator


class GeneratorAggregator:
    @staticmethod
    def mapper(file_path: str) -> Generator[tuple, None, None]:
        with open(file_path, "r") as file_to_read:
            for line in file_to_read:
                yield line.split(";")

    @staticmethod
    def reducer(
        input_generator: Generator[tuple, None, None], hash_map: Hash, tree: Tree
    ) -> None:
        for data in input_generator:
            hash_map[data[0]] = hash_map.get(data[0], 0) + int(data[1])
        for item in hash_map.traverse_keys():
            tree.root = tree.insert(item.key, item.val, tree.root)
