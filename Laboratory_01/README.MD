# Laboratory Activity 01: Python References & Complexity Profiling

## 1. Objectives
- Differentiate between mutable and immutable object references using the `id()` function.
- Demonstrate how variable assignment copies references, not data, causing side effects.
- Write a profiling program using Python's `time` module to measure execution time.
- Compare O(1), O(n), and O(n²) growth curves using microsecond measurements.

## 2. Execution & Output

### Task 1: Object ID and Mutable References
**Code:** [`task1_references.py`](task1_references.py)

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



