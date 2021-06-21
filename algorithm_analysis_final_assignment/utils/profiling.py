import time
import memory_profiler as mp
import matplotlib.pyplot as plt
import numpy as np


class Profiling:
    @staticmethod
    def execution_profiling(function):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            return_value = mp.memory_usage(
                proc=(function, args, kwargs), interval=0.5, retval=True
            )
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return {
                "return_value": return_value[1],
                "execution_time": execution_time,
                "memory_profiling": return_value[0],
            }

        return wrapper

    @staticmethod
    def plot_mem_profiling(
        data: dict,
        title: str,
        output_file_name: str = None,
        to_file: bool = True,
    ) -> None:
        max_mem = data["max_mem"]
        min_mem = data["min_mem"]
        avg_mem = data["avg_mem"]
        labels = data["labels"]
        x_range = np.arange(len(labels))

        width = 0.2
        fig, ax = plt.subplots()
        _ = ax.bar(x_range - width, max_mem, width, label="Max Memory Usage")
        _ = ax.bar(x_range, min_mem, width, label="Min Memory Usage")
        _ = ax.bar(x_range + width, avg_mem, width, label="Avg Memory Usage")

        ax.set_ylabel("Memory in MB")
        ax.set_title(title)
        ax.set_xticks(x_range)
        ax.set_xticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
        ax.legend()

        fig.tight_layout()

        if to_file:
            plt.savefig(output_file_name)
        else:
            plt.show()

    @staticmethod
    def plot_time_profiling(
        data: dict,
        title: str,
        output_file_name: str = None,
        to_file: bool = True,
    ) -> None:
        exec_time = data["time"]
        labels = data["labels"]
        x_range = np.arange(len(labels))

        width = 0.2
        fig, ax = plt.subplots()
        _ = ax.bar(x_range, exec_time, width, label="Avg Execution Time")

        ax.set_ylabel("Time in Seconds")
        ax.set_title(title)
        ax.set_xticks(x_range)
        ax.set_xticklabels(labels)
        plt.setp(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
        ax.legend()

        fig.tight_layout()

        if to_file:
            plt.savefig(output_file_name)
        else:
            plt.show()
