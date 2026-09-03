# Circular Queue Implementation

## Objectives

1. Implement a fixed-capacity Circular Queue from scratch in Python.
2. Understand index wrapping mathematical calculations using `(tail + 1) % capacity`.
3. Solve buffer overflow and underflow conditions with proper handling.

## Execution & Output

### Sample Program Run (Capacity = 5)

**Initial State:**
```
Queue array: [None, None, None, None, None] | Head: 0 | Tail: 0
```

**Operations Sequence:**
1. `enqueue(1)` → `Queue array: [1, None, None, None, None] | Head: 0 | Tail: 1`
2. `enqueue(2)` → `Queue array: [1, 2, None, None, None] | Head: 0 | Tail: 2`
3. `enqueue(3)` → `Queue array: [1, 2, 3, None, None] | Head: 0 | Tail: 3`
4. `dequeue()` → Returns `1`, `Queue array: [None, 2, 3, None, None] | Head: 1 | Tail: 3`
5. `enqueue(4)` → `Queue array: [None, 2, 3, 4, None] | Head: 1 | Tail: 4`

**Final Display:**
```
Queue array: [None, 2, 3, 4, None] | Head: 1 | Tail: 4
```


### Overflow & Underflow Tests

**Overflow Test (Capacity = 3):**
```
enqueue(10) → True
enqueue(20) → True
enqueue(30) → True
enqueue(40) → Overflow Warning: Queue is full. Cannot enqueue 40
```

**Underflow Test:**
```
dequeue() → 10
dequeue() → 20
dequeue() → 30
dequeue() → Underflow Warning: Queue is empty. Cannot dequeue
```


## Queue State Trace (10 Operations)

| Operation | Array State | Head | Tail | Size |
|-----------|-------------|------|------|------|
| Initial   | [N,N,N,N,N] | 0    | 0    | 0    |
| Enqueue 1 | [1,N,N,N,N] | 0    | 1    | 1    |
| Enqueue 2 | [1,2,N,N,N] | 0    | 2    | 2    |
| Enqueue 3 | [1,2,3,N,N] | 0    | 3    | 3    |
| Dequeue   | [N,2,3,N,N] | 1    | 3    | 2    |
| Enqueue 4 | [N,2,3,4,N] | 1    | 4    | 3    |
| Enqueue 5 | [N,2,3,4,5] | 1    | 0    | 4    |
| Dequeue   | [N,N,3,4,5] | 2    | 0    | 3    |
| Enqueue 6 | [6,N,3,4,5] | 2    | 1    | 4    |
| Enqueue 7 | [6,7,3,4,5] | 2    | 2    | 5    |
| Dequeue   | [6,7,N,4,5] | 3    | 2    | 4    |

*N = None*

## Report Analysis Questions

### 1. Purpose of the `%` (Modulo) Operator

The modulo operator `%` is essential in circular queue implementations for **index wrapping**. Here's why:

**Index Wrapping:** When the tail or head pointer reaches the end of the array (`capacity - 1`), the modulo operation wraps it back to 0:
```(tail + 1) % capacity```


**Example with capacity = 5:**
- `(4 + 1) % 5 = 0` → wraps from index 4 to index 0
- `(5 + 1) % 5 = 1` → continues from 0 to 1

**Why This Matters:**
1. **No Array Bounds Error:** Prevents accessing indices beyond the array's allocated memory.
2. **Automatic Wrap-Around:** The calculation handles the circular nature without conditional statements.
3. **Efficiency:** Single arithmetic operation instead of branching logic.
4. **Consistency:** The same formula works for both increment and decrement operations (by adding `capacity` before modulo for negative values).

**Without the Modulo:**
```python
# Without modulo (incorrect - would crash):
tail = tail + 1  # When tail = 4 (capacity-1), next would be 5 → IndexError

# With modulo (correct):
tail = (tail + 1) % capacity  # When tail = 4, next = 0 ✓
```

## Key Implementation Details Explained

### Why This Works

1. **`enqueue()` method:**
   - Checks `is_full()` before inserting
   - Places item at current `tail` position
   - Increments `size` counter
   - Updates `tail` using `(tail + 1) % capacity` for circular wrapping

2. **`dequeue()` method:**
   - Checks `is_empty()` before removing
   - Retrieves item at current `head` position
   - Sets position to `None` (cleanup)
   - Decrements `size` counter
   - Updates `head` using `(head + 1) % capacity` for circular wrapping

3. **The `size` variable** is crucial:
   - It tracks the actual number of elements (distinguishes empty vs full states)
   - Avoids the ambiguity where `head == tail` could mean either empty or full

### Running the Code

Save the solution above as `lab6_circular_queue.py` and run it: [lab6_circular_queue.py](lab6_circular_queue.py)


### Expected Output:
```
Dequeued: 1
Queue array: [None, 2, 3, 4, None] | Head: 1 | Tail: 4
```
