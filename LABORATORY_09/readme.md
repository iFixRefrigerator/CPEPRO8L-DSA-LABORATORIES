# Lab 9 — AVL Tree Height Balancing

## Objectives
1. Calculate height metrics and balance factors dynamically.
2. Implement Single and Double Rotations (LL, RR, LR, RL cases).
3. Demonstrate self-balancing tree insertions.

## Execution

```bash
python3 lab9_avl.py
```

### Output Snapshot

```
--- After inserting 30 ---
Root: 20 (h=2, bf=0)
    L--- 10 (h=1, bf=0)
    R--- 30 (h=1, bf=0)
```

| Insert Step | Root Key | Root BF | Root Height | Rotation Applied |
|-------------|----------|---------|-------------|------------------|
| 10          | 10       | 0       | 1           | None             |
| 20          | 10       | -1      | 2           | None             |
| 30          | 20       | 0       | 2           | Left (RR case)   |

---

## Report Analysis

### 1. AVL Insertion & Rotation Routines

**Insertion algorithm** (recursive):
1. Perform a standard BST insert.
2. Update the height of the current node: `1 + max(h(left), h(right))`.
3. Compute the balance factor: `bf = h(left) − h(right)`.
4. If `|bf| > 1`, apply one of four rotations:
   - **LL** (`bf > 1`, key < left.key) → single right rotation
   - **RR** (`bf < −1`, key > right.key) → single left rotation
   - **LR** (`bf > 1`, key > left.key) → left rotate left child, then right rotate node
   - **RL** (`bf < −1`, key < right.key) → right rotate right child, then left rotate node

**Rotation code** (from `rotate_right` and `rotate_left`) simply reassigns the three relevant pointers (`x`, `y`, `T2`) and updates the two affected node heights in the correct order — children first, then the new parent.

### 2. Sequence Diagram — Right Rotation (`rotate_right(y)`)

```
Before:                   After:
        y                       x
       / \                     / \
      x   T3    ───────►      T1   y
     / \                          / \
    T1  T2                       T2  T3
```

```
Client          AVLTree            y              x            T2
  │                │               │              │             │
  │ insert(key)    │               │              │             │
  ├───────────────►│               │              │             │
  │                │ rotate_right(y)              │             │
  │                ├──────────────►│              │             │
  │                │               │  x = y.left  │             │
  │                │               ├─────────────►│             │
  │                │               │  T2 = x.right│             │
  │                │               ├──────────────────────────►│
  │                │               │  x.right = y │             │
  │                │               ├─────────────►│             │
  │                │               │  y.left = T2 │             │
  │                │               ├──────────────────────────►│
  │                │               │  update y.height           │
  │                │               │  update x.height           │
  │                │◄──────────────┤ return x     │             │
  │◄───────────────┤               │              │             │
```

### 3. Trace — Inserting `[10, 20, 30]`

**Step 1 — insert(10)**
- Empty tree → new node `10`. Height = 1, bf = 0. No rotation.

**Step 2 — insert(20)**
- `20 > 10` → goes to right child of `10`.
- Heights: `20.h = 1`, `10.h = 2`. `bf(10) = 0 − 1 = −1`. Within range → no rotation.

**Step 3 — insert(30)**
- `30 > 10`, `30 > 20` → right child of `20`.
- Bubble up:
  - `20.h = 2`, `bf(20) = −1` ✔
  - `10.h = 3`, `bf(10) = 0 − 2 = −2` ✘ → **RR case** (right-right heavy)
- Apply **left rotation on node `10`**:
  ```
     10                    20
       \                   /  \
       20      ──►       10    30
         \
         30
  ```
- New root = `20`, height = 2, `bf(20) = 1 − 1 = 0`. ✔ Balanced.

**Final AVL tree:**
```
        20
       /  \
     10    30
```

Height dropped from 3 → 2, confirming O(log n) balance is restored automatically.

<br>

---

**Course:** CPEPR08L — Data Structures & Algorithms  
**Section:** BSCOME - 2  
**Name:** Robles, John Vincent M.

---
---
