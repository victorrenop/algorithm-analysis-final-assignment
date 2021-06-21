from algorithm_analysis_final_assignment.data_structures.hash.hash import Hash
from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree


class FileAggregator:
    @staticmethod
    def mapper(file_path: str) -> str:
        output_file = file_path.replace("/", "/mapped_")
        with open(file_path, "r") as file_to_read:
            with open(output_file, "w") as file_to_write:
                for line in file_to_read:
                    parsed_line = line.split(" ")
                    file_to_write.write("%s %s" % (parsed_line[0], parsed_line[1]))

        return output_file

    @staticmethod
    def reducer(execution_details: dict) -> str:
        hash_map = execution_details["hash_map"]
        file_path = execution_details["file"]
        output_file = file_path.replace("/mapped_", "/reduced_")
        with open(file_path, "r") as file_to_read:
            for line in file_to_read:
                parsed_line = line.split(" ")
                hash_map[parsed_line[0]] = hash_map.get(parsed_line[0], 0) + int(
                    parsed_line[1]
                )
        with open(output_file, "w") as file_to_write:
            for item in hash_map.traverse_keys():
                file_to_write.write("%s %s\n" % (item.key, item.val))

        return output_file

    @staticmethod
    def final_reducer(file_paths: list, hash_map: Hash, tree: Tree) -> None:
        for file_path in file_paths:
            with open(file_path, "r") as file_to_read:
                for line in file_to_read:
                    parsed_line = line.split(" ")
                    hash_map[parsed_line[0]] = hash_map.get(parsed_line[0], 0) + int(
                        parsed_line[1]
                    )
        for item in hash_map.traverse_keys():
            tree.root = tree.insert(item.key, item.val, tree.root)
