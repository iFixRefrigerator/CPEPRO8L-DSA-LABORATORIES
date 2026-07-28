# Laboratory Activity 02: Custom Dynamic Array Builder
---
## 1. Objectives
- Implement a custom dynamic array class from scratch using Python's `ctypes` module.
- Understand capacity scaling, memory doubling, and the cost of element copying.
- Observe how index access works in O(1) constant time complexity.
---
## 2. Execution & Output

**Code:** [`lab2_dynamic_array.py`](lab2_dynamic_array.py)

**Console Output:**
```
--- Starting append loop ---
Appending 0 | Size: 1 | Capacity: 1 | Element at index 0: 0
Resizing from 1 to 2
Appending 1 | Size: 2 | Capacity: 2 | Element at index 1: 1
Resizing from 2 to 4
Appending 2 | Size: 3 | Capacity: 4 | Element at index 2: 2
Appending 3 | Size: 4 | Capacity: 4 | Element at index 3: 3
Resizing from 4 to 8
Appending 4 | Size: 5 | Capacity: 8 | Element at index 4: 4
Appending 5 | Size: 6 | Capacity: 8 | Element at index 5: 5
Appending 6 | Size: 7 | Capacity: 8 | Element at index 6: 6
Appending 7 | Size: 8 | Capacity: 8 | Element at index 7: 7
Resizing from 8 to 16
Appending 8 | Size: 9 | Capacity: 16 | Element at index 8: 8
Appending 9 | Size: 10 | Capacity: 16 | Element at index 9: 9
```

### Resize Observations
- The array resizes when `size == capacity`.
- Resize occurs at capacities: **1 → 2 → 4 → 8 → 16** (doubling each time).
- After each resize, new elements can be added without immediate resizing.

---

## 3. Analysis Questions

**Question 1: At what sizes do capacity resizes occur?**  
- Resizes happen when the array reaches capacity: at **1, 2, 4, 8** (and would continue at 16, 32, etc.).

**Question 2: Why does the dynamic array copy elements during resize?**  
- Dynamic arrays must allocate a new, larger contiguous block of memory in the background. Python doesn't automatically extend the original block, so all existing elements must be copied to the new memory location to preserve their order and data.

**Question 3: What is the time complexity of a single resize operation?**  
- A single resize is **O(n)** because it loops through all `n` existing elements to copy them to the new array. However, because resizing happens infrequently (doubling), the *amortized* time for `append` is still **O(1)**.

---

## 4. Conclusions

By building this dynamic array manually, we observe that `append` operations are generally fast (O(1)), but occasionally trigger an expensive O(n) resize. Doubling the capacity reduces the number of resizes, making the array efficient overall.

---

## Files Included
- `lab2_dynamic_array.py` – Source code
- `README.md` – Lab report
