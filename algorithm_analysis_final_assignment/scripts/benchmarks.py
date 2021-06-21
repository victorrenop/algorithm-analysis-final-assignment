from pyspark.sql.dataframe import DataFrame
from algorithm_analysis_final_assignment.data_structures.tree.tree import Tree
from algorithm_analysis_final_assignment.data_structures.hash import (
    LinkedHash,
    OpenHash,
)
from algorithm_analysis_final_assignment.data_structures.tree import (
    AVLTree,
)
from algorithm_analysis_final_assignment.aggregator import (
    FileAggregator,
    GeneratorAggregator,
)
from algorithm_analysis_final_assignment.utils import FileUtils, Profiling
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from multiprocessing.dummy import Pool as ThreadPool

INPUT_FILE = "datasets/HIST_PAINEL_COVIDBR_2020_Parte1_09jun2021.csv"
SPARK_RESULT_DIR = "output/spark_result/"
HASH_MAP_SIZE = 500


@Profiling.execution_profiling
def run_file_map_reduce(
    hash_map_details: dict, tree: Tree, files: list, n_threads: int = 1
) -> dict:
    pool = ThreadPool(n_threads)
    mapped_files = pool.map(FileAggregator.mapper, files)
    reducer_execution_details = [
        {
            "hash_map": hash_map_details["class"](**hash_map_details["kwargs"]),
            "file": mapped_file,
        }
        for mapped_file in mapped_files
    ]
    reduced_files = pool.map(
        FileAggregator.reducer,
        reducer_execution_details,
    )
    tree = FileAggregator.final_reducer(
        reduced_files, hash_map_details["class"](**hash_map_details["kwargs"]), tree
    )

    return {"tree": tree, "files_to_clean": mapped_files + reduced_files}


@Profiling.execution_profiling
def run_generator_map_reduce(hash_map_details: dict, tree: Tree):
    hash_map = hash_map_details["class"](**hash_map_details["kwargs"])
    GeneratorAggregator.reducer(
        GeneratorAggregator.mapper("output/filtered_data.csv"), hash_map, tree
    )

    return {"tree": tree, "files_to_clean": []}


@Profiling.execution_profiling
def run_spark_map_reduce(spark: SparkSession, input_file: str) -> DataFrame:
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("delimiter", ";")
        .load(input_file)
    )
    df = df.select(["data", "casosNovos"]).withColumn(
        "casosNovos", col("casosNovos").cast("int")
    )
    df = (
        df.groupBy("data")
        .sum("casosNovos")
        .withColumnRenamed("sum(casosNovos)", "casosNovos")
        .sort("casosNovos", ascending=True)
    )
    _ = df.collect()

    return df


def update_bench_mark_data(
    benchmark_data: dict, label: str, mem_usage: list, exec_time: float
) -> None:
    benchmark_data["labels"].append(label)
    benchmark_data["max_mem"].append(max(mem_usage))
    benchmark_data["min_mem"].append(min(mem_usage))
    benchmark_data["avg_mem"].append(sum(mem_usage) / len(mem_usage))
    benchmark_data["time"].append(exec_time)


def build_test_profiling() -> dict:
    return {
        "generator": {
            "max_mem": [],
            "min_mem": [],
            "avg_mem": [],
            "time": [],
            "labels": [],
        },
        "single": {
            "max_mem": [],
            "min_mem": [],
            "avg_mem": [],
            "time": [],
            "labels": [],
        },
        "multi": {
            "max_mem": [],
            "min_mem": [],
            "avg_mem": [],
            "time": [],
            "labels": [],
        },
    }


def build_test_classes() -> dict:
    return {
        "linked_hash": [
            {
                "class": LinkedHash,
                "kwargs": {
                    "hash_map_size": HASH_MAP_SIZE,
                    "hash_function_selector": "division",
                },
            },
            {
                "class": LinkedHash,
                "kwargs": {
                    "hash_map_size": HASH_MAP_SIZE,
                    "hash_function_selector": "multiplication",
                },
            },
        ],
        "open_hash": [
            {
                "class": OpenHash,
                "kwargs": {
                    "hash_map_size": HASH_MAP_SIZE,
                    "hash_function_selector": "linear",
                },
            },
            {
                "class": OpenHash,
                "kwargs": {
                    "hash_map_size": HASH_MAP_SIZE,
                    "hash_function_selector": "quadratic",
                },
            },
            {
                "class": OpenHash,
                "kwargs": {
                    "hash_map_size": HASH_MAP_SIZE,
                    "hash_function_selector": "double",
                },
            },
        ],
    }


def run_bench_marks():
    execution_profiling_data = build_test_profiling()
    execution_details = build_test_classes()
    file_size = FileUtils.filter_and_write_csv(
        INPUT_FILE,
        separator=";",
        filter_cols=["data", "casosNovos"],
    )
    spark = SparkSession.builder.getOrCreate()
    print("Running benchmarks\n")
    print("Benchmark for Spark:")
    result = run_spark_map_reduce(spark, INPUT_FILE)
    for key in execution_profiling_data.keys():
        update_bench_mark_data(
            execution_profiling_data[key],
            "Spark Map Reduce",
            result["memory_profiling"],
            result["execution_time"],
        )
    result["return_value"].coalesce(1).write.mode("overwrite").option(
        "header", "false"
    ).option("delimiter", " ").csv(SPARK_RESULT_DIR)
    print("\tSpark Map Reduce took %s seconds" % (result["execution_time"]))
    print("Benchmark for generator map reduce:")
    for structure, details in execution_details.items():
        print("\tBenchmarks using %s:" % (structure))
        for detail in details:
            tree = AVLTree()
            result = run_generator_map_reduce(detail, tree)
            print(
                "\t\t%s with %s took %s seconds"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                    result["execution_time"],
                )
            )
            output_file = "output/generator_result_%s_%s.txt" % (
                detail["class"].__name__,
                detail["kwargs"]["hash_function_selector"],
            )
            FileUtils.output_tree_to_file(tree, output_file)
            update_bench_mark_data(
                execution_profiling_data["generator"],
                "%s-%s"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                ),
                result["memory_profiling"],
                result["execution_time"],
            )

    n_threads = 1
    files = FileUtils.split_csv_file("output/filtered_data.csv", file_size, n_threads)
    print("Benchmark for single threaded map reduce:")
    for structure, details in execution_details.items():
        print("\tBenchmarks using %s:" % (structure))
        for detail in details:
            tree = AVLTree()
            result = run_file_map_reduce(detail, tree, files, n_threads)
            print(
                "\t\t%s with %s took %s seconds"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                    result["execution_time"],
                )
            )
            FileUtils.cleanup_files(result["return_value"]["files_to_clean"])
            output_file = "output/single_thread_result_%s_%s.txt" % (
                detail["class"].__name__,
                detail["kwargs"]["hash_function_selector"],
            )
            FileUtils.output_tree_to_file(tree, output_file)
            update_bench_mark_data(
                execution_profiling_data["single"],
                "%s-%s"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                ),
                result["memory_profiling"],
                result["execution_time"],
            )

    n_threads = 4
    files = FileUtils.split_csv_file("output/filtered_data.csv", file_size, n_threads)
    print("Benchmark for %s threads map reduce:" % (n_threads))
    for structure, details in execution_details.items():
        print("\tBenchmarks using %s:" % (structure))
        for detail in details:
            tree = AVLTree()
            result = run_file_map_reduce(detail, tree, files, n_threads)
            print(
                "\t\t%s with %s took %s seconds"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                    result["execution_time"],
                )
            )
            FileUtils.cleanup_files(result["return_value"]["files_to_clean"])
            output_file = "output/multi_thread_result_%s_%s.txt" % (
                detail["class"].__name__,
                detail["kwargs"]["hash_function_selector"],
            )
            FileUtils.output_tree_to_file(tree, output_file)
            update_bench_mark_data(
                execution_profiling_data["multi"],
                "%s-%s"
                % (
                    detail["class"].__name__,
                    detail["kwargs"]["hash_function_selector"],
                ),
                result["memory_profiling"],
                result["execution_time"],
            )

    return execution_profiling_data


if __name__ == "__main__":
    execution_profiling_data = run_bench_marks()
    Profiling.plot_mem_profiling(
        execution_profiling_data["generator"],
        "Generator Benchmarks",
        "output/mem_generator.png",
    )
    Profiling.plot_time_profiling(
        execution_profiling_data["generator"],
        "Generator Benchmarks",
        "output/time_generator.png",
    )
    Profiling.plot_mem_profiling(
        execution_profiling_data["single"],
        "Single Thread Benchmarks",
        "output/mem_single.png",
    )
    Profiling.plot_time_profiling(
        execution_profiling_data["single"],
        "Single Thread Benchmarks",
        "output/time_single.png",
    )
    Profiling.plot_mem_profiling(
        execution_profiling_data["multi"],
        "Multi Thread Benchmarks",
        "output/mem_multi.png",
    )
    Profiling.plot_time_profiling(
        execution_profiling_data["multi"],
        "Multi Thread Benchmarks",
        "output/time_multi.png",
    )
