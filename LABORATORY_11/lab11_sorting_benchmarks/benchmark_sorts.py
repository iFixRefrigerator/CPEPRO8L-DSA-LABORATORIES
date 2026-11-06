"""Benchmark harness for Lab 11.

Task A (this file, for now): datasets, sizes, and the fairness plan.
Task D (later): the actual timing loop, median calculation, CSV and chart.

FAIRNESS CONTROLS (copy these into README.md later)
1. Same data for every algorithm: each (distribution, size) dataset is
   generated ONCE from a fixed random seed, then reused by all six algorithms.
2. Fresh copy per trial: every timed run receives list(source_data), so no
   algorithm ever sees data already sorted by an earlier run.
3. Setup excluded from timing: dataset generation and copying happen BEFORE
   the timer starts; only the sort call is timed.
4. Same clock: time.perf_counter() for every measurement.
5. Repeated trials: at least 3 per algorithm/condition; report the MEDIAN.
6. Correctness first: the benchmark only runs after test_sorts.py is clean.
7. Skips are recorded: if a quadratic algorithm exceeds the instructor's
   time limit, the run is skipped and the skip + reason are logged.
"""

import random

# Sizes: at least three. CONFIRM THESE WITH YOUR INSTRUCTOR before Task D.
BENCHMARK_SIZES = [1000, 2000, 5000]
TRIALS_PER_CONDITION = 3          # minimum required; 5 is better
SEED = 2026
DISTRIBUTIONS = ["random", "sorted", "reverse_sorted", "duplicate_heavy"]


def make_dataset(kind, size, seed=SEED):
    """Build one benchmark dataset of the given distribution and size."""
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(0, size * 10) for _ in range(size)]
    if kind == "sorted":
        return list(range(size))
    if kind == "reverse_sorted":
        return list(range(size, 0, -1))
    if kind == "duplicate_heavy":
        # only ~10 distinct values, so many repeats
        return [rng.randint(0, 9) for _ in range(size)]
    raise ValueError(f"Unknown dataset kind: {kind}")


def build_all_datasets():
    """Generate every (distribution, size) dataset exactly once."""
    return {
        (kind, size): make_dataset(kind, size)
        for kind in DISTRIBUTIONS
        for size in BENCHMARK_SIZES
    }


if __name__ == "__main__":
    datasets = build_all_datasets()
    print(f"Sizes: {BENCHMARK_SIZES} | trials: {TRIALS_PER_CONDITION}")
    for (kind, size), data in datasets.items():
        print(f"  {kind:16s} n={size:5d}  first 5: {data[:5]}")
