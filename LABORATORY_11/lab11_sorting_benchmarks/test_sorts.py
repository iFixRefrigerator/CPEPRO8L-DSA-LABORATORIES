"""Correctness tests for Lab 11 (Task A defines the datasets).

Run with:  python -m unittest test_sorts -v

The reference check uses Python's sorted() ONLY here, as an independent
answer key. It is never used inside sorting_algorithms.py.
"""

import copy
import random
import unittest

from sorting_algorithms import ALGORITHMS, new_stats


def build_correctness_datasets():
    """Required datasets: empty, one-item, duplicates, sorted, reverse, random."""
    rng = random.Random(11)  # fixed seed -> reproducible
    return {
        "empty": [],
        "one_item": [42],
        "two_items_swapped": [2, 1],
        "duplicates": [5, 3, 5, 1, 3, 5, 1, 1, 3],
        "all_equal": [7] * 10,
        "already_sorted": list(range(20)),
        "reverse_sorted": list(range(20, 0, -1)),
        "random_values": [rng.randint(-100, 100) for _ in range(50)],
        "negatives_and_zero": [0, -5, 3, -1, 0, 8, -5],
    }


DATASETS = build_correctness_datasets()


class TestSortingAlgorithms(unittest.TestCase):
    def test_all_algorithms_on_all_datasets(self):
        for algo_name, algo in ALGORITHMS.items():
            for data_name, data in DATASETS.items():
                with self.subTest(algorithm=algo_name, dataset=data_name):
                    original = copy.deepcopy(data)
                    result = algo(copy.deepcopy(data), new_stats())
                    self.assertEqual(result, sorted(original))

    def test_input_is_not_modified(self):
        for algo_name, algo in ALGORITHMS.items():
            with self.subTest(algorithm=algo_name):
                data = [4, 2, 9, 1]
                snapshot = list(data)
                algo(data)
                self.assertEqual(data, snapshot)

    def test_stats_are_optional(self):
        for algo_name, algo in ALGORITHMS.items():
            with self.subTest(algorithm=algo_name):
                self.assertEqual(algo([3, 1, 2]), [1, 2, 3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
