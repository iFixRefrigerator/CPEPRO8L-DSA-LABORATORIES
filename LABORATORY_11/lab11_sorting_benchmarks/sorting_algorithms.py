"""Six sorting algorithms implemented from scratch (no built-in sorting).

Every function takes a list and returns a tuple:
    (sorted_list, comparisons, movements)
The input list is never modified; each function sorts a copy.

Counting rules (the same for all six, so results are comparable):
    comparison : one comparison between two data items
    movement   : one assignment of a data item; a swap counts as 3 movements
                 (three assignments), a shift or placement counts as 1

Summary:
    Bubble / Selection / Insertion : in place, O(n^2) time (Bubble and
                                     Insertion are O(n) on sorted data)
    Merge : O(n log n) time, O(n) auxiliary space
    Quick : O(n log n) average time, median-of-three pivot with a
            three-way partition, O(log n) auxiliary stack space
    Heap  : O(n log n) time, O(1) auxiliary space
(The copy of the input that each function returns is not counted as
auxiliary space.)
"""


def bubble_sort(arr):
    """Bubble Sort with early exit when a pass makes no swaps.

    Time O(n^2) worst/average, O(n) best. Space O(1).
    """
    a = arr[:]
    comps = moves = 0
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                moves += 3
                swapped = True
        if not swapped:
            break
    return a, comps, moves


def selection_sort(arr):
    """Selection Sort: select the minimum of the unsorted part each pass.

    Time O(n^2) in every case. Space O(1). At most n - 1 swaps.
    """
    a = arr[:]
    comps = moves = 0
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            moves += 3
    return a, comps, moves


def insertion_sort(arr):
    """Insertion Sort: shift larger items right and insert each key.

    Time O(n^2) worst/average, O(n) best (already sorted). Space O(1).
    """
    a = arr[:]
    comps = moves = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        moves += 1
    return a, comps, moves


def merge_sort(arr):
    """Top-down Merge Sort (stable: ties take the left item first).

    Time O(n log n) in every case. Space O(n) auxiliary (the merged lists
    and slices), which is the trade-off against in-place sorts.
    """
    a = arr[:]
    stats = {"comps": 0, "moves": 0}

    def _merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            stats["comps"] += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            stats["moves"] += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        stats["moves"] += len(left) - i + len(right) - j
        return merged

    def _sort(part):
        if len(part) <= 1:
            return part
        mid = len(part) // 2
        return _merge(_sort(part[:mid]), _sort(part[mid:]))

    a = _sort(a)
    return a, stats["comps"], stats["moves"]


def quick_sort(arr):
    """Quick Sort: median-of-three pivot, three-way partition.

    Pivot strategy: the pivot VALUE is the median of the first, middle and
    last items, which avoids the worst case on sorted and reverse-sorted data.

    Partition: items are split into  < pivot | == pivot | > pivot  (Dutch
    national flag). The == block is never sorted again, so lists with many
    duplicates (or all-equal lists) stay fast. A plain two-way Lomuto
    partition degrades to O(n^2) with deep recursion on such data.

    Space: it recurses on the SMALLER part and loops on the larger part, so
    the stack depth is at most O(log n). Time O(n log n) average, O(n^2)
    worst case (rare with a median-of-three pivot).
    """
    a = arr[:]
    stats = {"comps": 0, "moves": 0}

    def _median_of_three(lo, hi):
        mid = (lo + hi) // 2
        x, y, z = a[lo], a[mid], a[hi]
        stats["comps"] += 2
        if x < y:
            if y < z:
                return y
            stats["comps"] += 1
            return z if x < z else x
        stats["comps"] += 1
        if x < z:
            return x
        stats["comps"] += 1
        return z if y < z else y

    def _sort(lo, hi):
        while lo < hi:
            pivot = _median_of_three(lo, hi)
            lt, i, gt = lo, lo, hi
            while i <= gt:
                stats["comps"] += 1
                if a[i] < pivot:
                    if lt != i:
                        a[lt], a[i] = a[i], a[lt]
                        stats["moves"] += 3
                    lt += 1
                    i += 1
                else:
                    stats["comps"] += 1
                    if a[i] > pivot:
                        if i != gt:
                            a[i], a[gt] = a[gt], a[i]
                            stats["moves"] += 3
                        gt -= 1
                    else:
                        i += 1
            # now: a[lo:lt] < pivot, a[lt:gt+1] == pivot, a[gt+1:hi+1] > pivot
            if lt - lo < hi - gt:
                _sort(lo, lt - 1)
                lo = gt + 1
            else:
                _sort(gt + 1, hi)
                hi = lt - 1

    _sort(0, len(a) - 1)
    return a, stats["comps"], stats["moves"]


def heap_sort(arr):
    """Heap Sort: build a max-heap, then repeatedly move the max to the end.

    Time O(n log n) in every case. Space O(1) auxiliary. Not stable.
    """
    a = arr[:]
    comps = moves = 0
    n = len(a)

    def _sift_down(root, end):
        nonlocal comps, moves
        while True:
            child = 2 * root + 1
            if child > end:
                break
            if child + 1 <= end:
                comps += 1
                if a[child] < a[child + 1]:
                    child += 1
            comps += 1
            if a[root] < a[child]:
                a[root], a[child] = a[child], a[root]
                moves += 3
                root = child
            else:
                break

    for start in range(n // 2 - 1, -1, -1):
        _sift_down(start, n - 1)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        moves += 3
        _sift_down(0, end - 1)
    return a, comps, moves


ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}
