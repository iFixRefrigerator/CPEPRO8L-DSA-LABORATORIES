"""Sorting algorithms for Lab 11.

Task A: only the interface is defined here. You implement the bodies in
Task B (elementary sorts) and Task C (advanced sorts).

Shared interface (every function follows it):
    sort_name(data, stats=None) -> list

    data  : list of comparable items. The input list must NOT be modified;
            work on a copy and return the sorted copy.
    stats : optional dict used to count work, e.g.
            {"comparisons": 0, "moves": 0}
            If None, counting is simply skipped.

Built-in sorting (sorted(), list.sort()) is NOT allowed in this module.
"""


def new_stats():
    """Return a fresh counter dictionary for one sorting run."""
    return {"comparisons": 0, "moves": 0}


# ---------- Task B: elementary sorts ----------

def bubble_sort(data, stats=None):
    """Sort using Bubble Sort. Expected: O(n^2) time, O(1) extra space."""
    raise NotImplementedError("Task B")


def selection_sort(data, stats=None):
    """Sort using Selection Sort. Expected: O(n^2) time, O(1) extra space."""
    raise NotImplementedError("Task B")


def insertion_sort(data, stats=None):
    """Sort using Insertion Sort. Expected: O(n^2) worst, O(n) best."""
    raise NotImplementedError("Task B")


# ---------- Task C: advanced sorts ----------

def merge_sort(data, stats=None):
    """Sort using Merge Sort. Expected: O(n log n) time, O(n) extra space."""
    raise NotImplementedError("Task C")


def quick_sort(data, stats=None):
    """Sort using Quick Sort. Document your pivot strategy here."""
    raise NotImplementedError("Task C")


def heap_sort(data, stats=None):
    """Sort using Heap Sort. Expected: O(n log n) time, O(1) extra space."""
    raise NotImplementedError("Task C")


# Registry used by the tests and the benchmark so both stay in sync.
ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}
