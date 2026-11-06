"""Correctness tests for Lab 11.

Run with:  python -m unittest test_sorts -v

sorted() is used ONLY here, as an independent answer key. It must never
appear inside sorting_algorithms.py (a test below checks that).
"""

import copy
import random
import re
import unittest
from pathlib import Path

from sorting_algorithms import ALGORITHMS


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


def build_large_datasets():
    """Benchmark-sized data, including cases that break naive Quick Sort."""
    rng = random.Random(12)
    n = 5000
    return {
        "large_random": [rng.randint(0, n * 10) for _ in range(n)],
        "large_sorted": list(range(n)),
        "large_reverse": list(range(n, 0, -1)),
        "large_duplicate_heavy": [rng.randint(0, 9) for _ in range(n)],
        "large_all_equal": [7] * n,
    }


DATASETS = build_correctness_datasets()
LARGE_DATASETS = build_large_datasets()
SLOW_ALGORITHMS = {"bubble", "selection", "insertion"}


class TestSortingAlgorithms(unittest.TestCase):
    def test_all_algorithms_on_required_datasets(self):
        for algo_name, algo in ALGORITHMS.items():
            for data_name, data in DATASETS.items():
                with self.subTest(algorithm=algo_name, dataset=data_name):
                    result, comps, moves = algo(copy.deepcopy(data))
                    self.assertEqual(result, sorted(data))
                    self.assertGreaterEqual(comps, 0)
                    self.assertGreaterEqual(moves, 0)

    def test_large_datasets(self):
        """Catches RecursionError / O(n^2) blowups, mainly in Quick Sort."""
        for algo_name, algo in ALGORITHMS.items():
            for data_name, data in LARGE_DATASETS.items():
                if algo_name in SLOW_ALGORITHMS and data_name == "large_random":
                    continue  # keep the test run fast; covered by smaller sets
                with self.subTest(algorithm=algo_name, dataset=data_name):
                    result, _, _ = algo(list(data))
                    self.assertEqual(result, sorted(data))

    def test_input_is_not_modified(self):
        for algo_name, algo in ALGORITHMS.items():
            with self.subTest(algorithm=algo_name):
                data = [4, 2, 9, 1]
                snapshot = list(data)
                algo(data)
                self.assertEqual(data, snapshot)

    def test_counters_on_sorted_input(self):
        """Bubble and Insertion should be near-linear on sorted data."""
        data = list(range(100))
        for name in ("bubble", "insertion"):
            with self.subTest(algorithm=name):
                _, comps, _ = ALGORITHMS[name](data)
                self.assertLessEqual(comps, 200)

    def test_no_builtin_sorting_in_module(self):
        source = Path(__file__).with_name("sorting_algorithms.py").read_text()
        code = "\n".join(
            line for line in source.splitlines()
            if not line.lstrip().startswith("#")
        )
        code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
        self.assertNotRegex(code, r"\bsorted\s*\(")
        self.assertNotRegex(code, r"\.sort\s*\(")


if __name__ == "__main__":
    unittest.main(verbosity=2)
