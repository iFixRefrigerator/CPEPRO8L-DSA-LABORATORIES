# Laboratory Activity No. 7: Recursion Tracing & Binary Search

**Course Code:** CPEPRO8L  
**Course Title:** Data Structures and Algorithms  
**Term:** First Semester, AY 2026–2027

---

## Objectives

1. Understand recursive execution, base cases, and call nesting.
2. Code and test recursive Binary Search.
3. Compare iterative and recursive space complexities.

---

## Source Code

### `lab7_recursive_search.py`

```python
def recursive_binary_search(arr, low, high, target):
    # Base Case: target is not in the array
    if low > high:
        return -1

    # Find middle index
    mid = (low + high) // 2

    # Base Case: target found
    if arr[mid] == target:
        return mid

    # If middle element is greater than target, search left half
    elif arr[mid] > target:
        return recursive_binary_search(arr, low, mid - 1, target)

    # Otherwise, search right half
    else:
        return recursive_binary_search(arr, mid + 1, high, target)


if __name__ == "__main__":
    data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target_val = 23

    result = recursive_binary_search(data, 0, len(data) - 1, target_val)
    print(f"Element found at index: {result}")
```

---

## Execution & Output

### Sample Run: Searching for `23`

Command:

```bash
python lab7_recursive_search.py
```

Output:

```text
Element found at index: 5
```

### Additional Test: Searching for `56`

Test code:

```python
data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
target_val = 56

result = recursive_binary_search(data, 0, len(data) - 1, target_val)
print(f"Element found at index: {result}")
```

Output:

```text
Element found at index: 7
```

---

## Recursion Trace for Searching `56`

Given array:

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Value | 2 | 5 | 8 | 12 | 16 | 23 | 38 | 56 | 72 | 91 |

Target: `56`

| Call | Arguments | `low` | `high` | `mid` | `arr[mid]` | Action |
|---|---:|---:|---:|---:|---:|---|
| 1 | `recursive_binary_search(arr, 0, 9, 56)` | 0 | 9 | 4 | 16 | `16 < 56`, search right half |
| 2 | `recursive_binary_search(arr, 5, 9, 56)` | 5 | 9 | 7 | 56 | `56 == 56`, return `7` |

---

## Execution Stack Trace Diagram

At the deepest point of recursion, the call stack looks like this:

```text
Top of stack / most recent call
+------------------------------------------------+
| recursive_binary_search(arr, 5, 9, 56)         |
| low = 5, high = 9, mid = 7                     |
| arr[7] = 56 == target                          |
| returns 7                                      |
+------------------------------------------------+
| recursive_binary_search(arr, 0, 9, 56)         |
| low = 0, high = 9, mid = 4                     |
| arr[4] = 16 < 56                               |
| waiting for result from recursive call         |
+------------------------------------------------+
Bottom of stack / first call
```

After the second call returns `7`, the first call receives that value and also returns `7`. The stack then unwinds and becomes empty.

---

## Report Analysis Questions

### 1. Draw the execution stack trace diagram showing the arguments passed to each call when searching for `56`.

```text
recursive_binary_search(arr, 0, 9, 56)
│
│  mid = 4
│  arr[4] = 16
│  16 < 56, so search right half
│
└──> recursive_binary_search(arr, 5, 9, 56)
     │
     │  mid = 7
     │  arr[7] = 56
     │  56 == 56, target found
     │
     └──> return 7
```

The arguments passed are:

1. First call: `arr, low=0, high=9, target=56`
2. Second call: `arr, low=5, high=9, target=56`

The second call returns `7`, which is the index of `56`.

### 2. Discuss why missing base cases lead to stack overflow errors.

A recursive function must have at least one base case that stops the recursion. In recursive Binary Search, the important base cases are:

1. `if low > high: return -1` — the target is not in the array.
2. `if arr[mid] == target: return mid` — the target is found.

If the `low > high` base case is missing, the function will continue calling itself even after the search range becomes invalid. Each recursive call pushes a new stack frame onto the call stack. Since the call stack has limited memory, the frames accumulate until the program raises a `RecursionError` in Python or a stack overflow error in lower-level languages.

For example, if the target is not present, eventually `low` becomes greater than `high`. Without the `low > high` check, the function may keep calling itself with invalid or repeated bounds, never terminating.

If the `arr[mid] == target` base case is missing, the function may fail to return the correct index even when the target exists. If both base cases are missing, the recursion is guaranteed to continue indefinitely or until the stack overflows.

Therefore, base cases are essential because they define when the recursion should stop and return a result.

---

## Iterative vs Recursive Space Complexity

| Algorithm | Time Complexity | Auxiliary Space Complexity |
|---|---:|---:|
| Iterative Binary Search | `O(log n)` | `O(1)` |
| Recursive Binary Search | `O(log n)` | `O(log n)` |

The iterative version uses only a few variables such as `low`, `high`, and `mid`, so its auxiliary space is constant. The recursive version uses the system call stack, and each recursive call creates a new stack frame. Since Binary Search halves the search space each time, the maximum recursion depth is approximately `O(log n)`.

---

## Conclusion

In this laboratory activity, I implemented recursive Binary Search and traced its recursive calls. The function correctly finds the target by repeatedly dividing the search range in half. I also learned that recursive algorithms require proper base cases to avoid infinite recursion and stack overflow errors. Finally, I compared iterative and recursive Binary Search, noting that both have `O(log n)` time complexity, but the recursive version uses `O(log n)` auxiliary space due to the call stack.
