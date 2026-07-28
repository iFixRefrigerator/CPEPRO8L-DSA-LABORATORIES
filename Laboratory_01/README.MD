# Laboratory Activity 01: Python References & Complexity Profiling

---

## 1. Objectives
- Differentiate between mutable and immutable object references using the `id()` function.
- Demonstrate how variable assignment copies references, not data, causing side effects.
- Write a profiling program using Python's `time` module to measure execution time.
- Compare O(1), O(n), and O(n²) growth curves using microsecond measurements.

---

## 2. Execution & Output

### Task 1: Object ID and Mutable References
**Code:** [`task1_reference.py`](task1_reference.py)

**Console Output:**
```
TASK 1: OBJECT ID COMPARISON
Address of list_a (id): 500339108224
Address of list_b (id): 500339108224
Are list_a and list_b pointing to the same object? True

After appending 40 to list_b:
list_a: [10, 20, 30, 40]
list_b: [10, 20, 30, 40]

After reassigning list_b to a new list:
list_a: [10, 20, 30, 40]
list_b: [100, 200]

New address of list_b (id): 500336473856
Address of list_a (id): 500339108224
Are list_a and list_b now the same? False
```

## Task 2: Execution Profiling (O(1), O(n), O(n²))
**Code:** [`task2_profiling.py`](task2_profiling.py)

**Benchmarking Table (in microseconds):**

| N      | O(1) (µs) | O(n) (µs) |  O(n²) (µs)  |
|--------|-----------|-----------|--------------|
| 100    |  [7.86]   | [10.05]   | [4612.60]    |
| 500    |  [9.22]   | [30.99]   | [88852.18]   |
| 1000   |  [5.73]   | [59.01]   | [355966.41]  |
| 5000   |  [9.17]   | [287.81]  | [9263759.48] |
| 10000  |  [44.58]  | [712.71]  | SKIPPED      |

---

## 3. Analysis Questions

### Question 1: Why did `list_a` change when appending to `list_b`?
`list_b = list_a` copies the **reference**, not the actual data. Both variables point to the exact same list object in memory. When we appended `40` to `list_b`, we mutated the shared object, so `list_a` reflected the change because it points to the same memory address.

### Question 2: What happens when assigning a new list to `list_b`?
When we executed `list_b = [100, 200]`, Python created a brand new list object in memory. `list_b` now points to this new object (different `id()`), while `list_a` continues to point to the original list `[10, 20, 30, 40]`. The reference link is permanently broken.

### Question 3: How does Big-O translate to actual execution speed?
- **O(1)**: Constant time — the operation takes roughly the same microseconds regardless of N.
- **O(n)**: Linear time — as N doubles, runtime roughly doubles.
- **O(n²)**: Quadratic time — as N doubles, runtime roughly quadruples. This becomes extremely slow for large N, which is why N=10000 was skipped.

---

## 4. Conclusions
Understanding object references is crucial in Python to prevent unintended side effects when building complex data structures like linked lists or trees. Additionally, theoretical Big-O analysis is validated by real profiling — O(n²) algorithms are impractical for large datasets, while O(1) and O(n) remain efficient. This lab demonstrates that mathematical complexity translates directly into measurable execution time differences on actual hardware.

## Files Included
- `task1_reference.py` – Source code for Task 1
- `task2_profiling.py` – Source code for Task 2
- `README.md` – This lab report
