from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree
import pandas as pd
import os


class FileUtils:
    @staticmethod
    def filter_and_write_csv(csv_path: str, separator: str, filter_cols: list) -> int:
        df = pd.read_csv(csv_path, sep=separator)
        df = df[filter_cols]
        df.to_csv("output/filtered_data.csv", sep=separator, header=False, index=False)

        return len(df.index)

    @staticmethod
    def split_csv_file(csv_path: str, file_size: int, parts: int = 1) -> list:
        part_count = 0
        files = []
        with open(csv_path, "r") as input_file:
            chunk_limit = int(((file_size / parts) * (part_count + 1)) - 1)
            file_descriptor = open("output/part_%s.csv" % (part_count + 1), "w")
            for idx, line in enumerate(input_file):
                if idx > chunk_limit:
                    files.append(file_descriptor.name)
                    file_descriptor.close()
                    part_count += 1
                    file_descriptor = open("output/part_%s.csv" % (part_count + 1), "w")
                    chunk_limit = int(((file_size / parts) * (part_count + 1)) - 1)
                file_descriptor.write(line.replace(";", " "))
        files.append(file_descriptor.name)
        file_descriptor.close()

        return files

    @staticmethod
    def cleanup_files(file_paths: list) -> None:
        for file_path in file_paths:
            os.remove(file_path)

    @staticmethod
    def output_tree_to_file(tree: Tree, output_file: str) -> None:
        with open(output_file, "w") as file_to_write:
            for item in tree.traverse_in_order(tree.root):
                file_to_write.write("%s %s\n" % (item.key, item.val))
