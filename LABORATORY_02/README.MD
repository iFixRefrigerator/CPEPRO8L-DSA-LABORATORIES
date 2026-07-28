# Laboratory Activity 02: Custom Dynamic Array Builder

## 1. Objectives
- Implement a custom dynamic array class from scratch using Python's `ctypes` module.
- Understand capacity scaling, memory doubling, and the cost of element copying.
- Observe how index access works in O(1) constant time complexity.

## 2. Execution & Output

**Code:** [`lab2_dynamic_array.py`](lab2_dynamic_array.py)

**Console Output:**
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
