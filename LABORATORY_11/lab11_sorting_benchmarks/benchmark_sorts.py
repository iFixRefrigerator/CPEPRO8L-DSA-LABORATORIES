"""
Benchmark driver for Lab 11.

Run with:  python benchmark_sorts.py
Outputs:   results.csv (raw data) and comparison_chart.png (runtime growth)

- Sizes: 100, 500, 1000, 2000 (adjust to workstation; confirm with instructor)
- Distributions: random, sorted, reverse, duplicates
- 3 trials per (algorithm, size, distribution); median reported
- Quadratic algorithms skipped above a configurable threshold (logged in CSV)

FAIRNESS CONTROLS
1. Same data for every algorithm: each (distribution, size) dataset is
   generated once from a fixed seed and reused by all six algorithms.
2. Fresh copy per trial: every timed run receives its own list(source), so
   no run ever sees data touched by an earlier run.
3. Setup excluded from timing: dataset generation, copying and the
   correctness check happen outside the timer; only the sort call is timed.
4. Same clock for everything: time.perf_counter().
5. Repeated trials (3) with the MEDIAN reported, to reduce the effect of
   background noise on a single run.
6. Correctness is checked on every run; a wrong result stops the benchmark.
7. Skips are recorded in the CSV with the reason.
"""
import csv
import time
import random
import statistics
from sorting_algorithms import ALGORITHMS

SIZES = [100, 500, 1000, 2000]
DISTRIBUTIONS = ["random", "sorted", "reverse", "duplicates"]
QUADRATIC = {"bubble", "selection", "insertion"}
QUADRATIC_MAX_N = 2000        # skip above this for O(n^2)
TRIALS = 3
SEED = 42


def make_dataset(kind, n, seed=SEED):
    rng = random.Random(seed + n)
    if kind == "random":
        return [rng.randint(0, 10_000) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "duplicates":
        return [rng.randint(0, max(1, n // 10)) for _ in range(n)]
    raise ValueError(kind)


def time_once(func, data, expected):
    """Time one sort call on `data` (a fresh copy); check the result after."""
    t0 = time.perf_counter()
    result, comps, moves = func(data)
    elapsed = time.perf_counter() - t0
    if result != expected:          # outside the timed region
        raise RuntimeError(f"{func.__name__} produced an incorrect result")
    return elapsed, comps, moves


def run():
    rows = []
    for kind in DISTRIBUTIONS:
        for n in SIZES:
            source = make_dataset(kind, n)
            expected = sorted(source)   # answer key, computed once, untimed
            for name, func in ALGORITHMS.items():
                if name in QUADRATIC and n > QUADRATIC_MAX_N:
                    rows.append(dict(
                        algorithm=name, distribution=kind, size=n,
                        median_time_s=None, comparisons=None,
                        movements=None, trials=0,
                        note=f"skipped: quadratic n>{QUADRATIC_MAX_N}"))
                    print(f"[SKIP] {name:10s} {kind:10s} n={n}")
                    continue
                times, comps_l, moves_l = [], [], []
                for _ in range(TRIALS):
                    fresh = list(source)    # fresh copy, made before timing
                    t, c, m = time_once(func, fresh, expected)
                    times.append(t); comps_l.append(c); moves_l.append(m)
                rows.append(dict(
                    algorithm=name, distribution=kind, size=n,
                    median_time_s=round(statistics.median(times), 8),
                    comparisons=int(statistics.median(comps_l)),
                    movements=int(statistics.median(moves_l)),
                    trials=TRIALS, note=""))
                print(f"[OK]   {name:10s} {kind:10s} n={n:<5d} "
                      f"median={statistics.median(times):.4f}s")

    with open("results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print("\nWrote results.csv")
    return rows


def make_chart(rows, path="comparison_chart.png"):
    """One panel per distribution: median runtime vs input size (log y)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; run: pip install matplotlib")
        return
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    for ax, kind in zip(axes.flat, DISTRIBUTIONS):
        for name in ALGORITHMS:
            pts = [(r["size"], r["median_time_s"]) for r in rows
                   if r["algorithm"] == name and r["distribution"] == kind
                   and r["median_time_s"]]
            if pts:
                xs, ys = zip(*pts)
                ax.plot(xs, ys, marker="o", label=name)
        ax.set_yscale("log")
        ax.set_title(f"{kind} data")
        ax.set_xlabel("input size n")
        ax.set_ylabel("median runtime (s, log scale)")
        ax.grid(True, alpha=0.3)
    axes[0, 0].legend()
    fig.suptitle("Sorting runtime growth by input distribution")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    print(f"Wrote {path}")


if __name__ == "__main__":
    make_chart(run())
