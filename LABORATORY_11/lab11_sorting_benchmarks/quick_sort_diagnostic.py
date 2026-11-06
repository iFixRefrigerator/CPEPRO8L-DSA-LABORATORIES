"""Diagnostic for guide question 6: why is Quick Sort slower on sorted and
reverse data than on random data?

Run with:  python quick_sort_diagnostic.py

It repeats the Quick Sort partitioning (median-of-three pivot, three-way
partition) on the same n=2000 datasets used by the benchmark, and reports:
  - total elements scanned by all partition steps (work done)
  - average balance of the split on partitions of 50+ items
    (0.5 = perfectly even halves, near 0 = very lopsided)
The results are deterministic, so they are the same on every machine.
"""
import statistics
from benchmark_sorts import make_dataset, DISTRIBUTIONS

N = 2000


def median_value(a, lo, hi):
    mid = (lo + hi) // 2
    x, y, z = a[lo], a[mid], a[hi]
    if x < y:
        return y if y < z else (z if x < z else x)
    return x if x < z else (z if y < z else y)


def analyse(data):
    a = list(data)
    scanned = 0
    balances = []

    def sort(lo, hi):
        nonlocal scanned
        while lo < hi:
            pivot = median_value(a, lo, hi)
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            left, right = lt - lo, hi - gt
            scanned += hi - lo + 1
            if hi - lo + 1 >= 50 and left + right:
                balances.append(min(left, right) / (left + right))
            if left < right:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(a) - 1)
    return scanned, statistics.mean(balances)


if __name__ == "__main__":
    print(f"n = {N}")
    print(f"{'distribution':12s} {'elements scanned':>17s} {'avg split balance':>18s}")
    for kind in DISTRIBUTIONS:
        scanned, balance = analyse(make_dataset(kind, N))
        print(f"{kind:12s} {scanned:17,d} {balance:18.3f}")
