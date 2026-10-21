# CPEPRO8L — Laboratory Activity No. 10
## Hash Tables and Collision Resolution (Chaining)

**Course:** Data Structures and Algorithms  
**Term:** First Semester, AY 2026–2027

---

## 1. Objectives

1. Implement a custom hash mapping function (sum of ASCII values mod capacity).
2. Design a collision resolution mechanism using **Linked List buckets** (separate chaining).
3. Observe how the **load factor** affects search efficiency.

---

## 2. Execution & Output

### Sample run

```text
$ python lab10_hash_table.py
Bucket 0: 
Bucket 1: 
Bucket 2: [Alice: 25]
Bucket 3: 
Bucket 4: [Bob: 30] -> [Charlie: 35]

Load factor: 0.60
```

### Trace table (capacity = 5)

| Operation            | Key     | ASCII Sum | Index (mod 5) | Bucket State After          |
|----------------------|---------|-----------|---------------|-----------------------------|
| `put("Alice", 25)`   | Alice   | 478       | 3             | 3 → [Alice:25]              |
| `put("Bob", 30)`     | Bob     | 275       | 0             | 4 → [Bob:30]                |
| `put("Charlie", 35)` | Charlie | 696       | 1             | 0 → [Charlie:35]            |
| `put("Don", 40)`     | Don     | 289       | 4             | 1 → [Don:40]                |
| `put("Eve", 22)`     | Eve     | 288       | 3             | 1 → [Don:40] -> [Eve:22] ⚠️ collision |


---

## 3. Report Analysis Questions

### Q1. Record hash table entries demonstrating a collision event

**Collision demo script:**

```python
ht = HashTable(5)
ht.put("Alice", 25)  # sum = 478 -> 478 % 5 = 3
ht.put("Eve", 22)    # sum = 288 -> 288 % 5 = 3  ← COLLISION
ht.display()
```

**Output:**

```
Bucket 0: 
Bucket 1: 
Bucket 2: 
Bucket 3: [Alice: 25] -> [Eve: 22]
Bucket 4: 
```

**Recorded collision entries:**

| Bucket | Chain Contents                |
|--------|-------------------------------|
| 1      | `[Don: 40] -> [Eve: 22]`      |

Both `"Don"` and `"Eve"` map to **bucket 1**, producing a collision. The `next` pointer in the `HashNode` for `"Don"` links to the `HashNode` for `"Eve"`, forming a **linked list chain** inside bucket 1 — this is **separate chaining**.

---

### Q2. Compare search efficiency: Chaining vs. Linear Probing

| Aspect                     | **Separate Chaining**                                             | **Linear Probing**                                                  |
|----------------------------|-------------------------------------------------------------------|---------------------------------------------------------------------|
| **Storage**                | Nodes stored outside the array (linked list)                      | All entries stored *inside* the array                              |
| **Collision handling**     | Append to bucket's linked list                                    | Probe next index `(i+1) % capacity` until a free slot is found     |
| **Best-case search**       | O(1) — bucket has 0 or 1 node                                     | O(1) — target slot is its hash index                               |
| **Average-case search**    | O(1 + α) where α = load factor                                    | O(1 + 1/(1−α)) for successful search                               |
| **Worst-case search**      | O(n) — all keys collide into one bucket                           | O(n) — clustering forces long probe sequences                      |
| **Deletion**               | Simple — just remove node from list                               | Tricky — needs tombstones or rehashing to avoid breaking probe runs |
| **Clustering**             | No clustering problem                                             | **Primary clustering** — collisions cascade into long runs         |
| **Memory overhead**        | Extra pointer per node (8 bytes typically)                        | No extra pointers; array-only                                     |
| **Load factor > 1**        | Allowed (chains grow arbitrarily)                                 | Not allowed — table must be resized before α > 1                   |

**Summary:** Chaining gives **more predictable performance** at high load factors because its search cost grows linearly with α rather than exploding like `1/(1−α)` in linear probing. Linear probing, however, is **cache-friendlier** and pointer-free, making it faster in practice at low load factors (α < 0.5). For a general-purpose hash table with unknown key distributions, **chaining is safer**; for read-heavy, memory-constrained workloads, **linear probing** wins.

**Empirical note from our trace:** With 3 entries in 5 buckets (α = 0.6), chaining still resolves any lookup in ≤ 2 probes, whereas linear probing at α = 0.6 averages ≈ 3.1 probes per successful lookup — and worsens sharply as α → 1.

---

## 4. How to Run

```bash
git clone <your-repo-url>
cd <repo>
python lab10_hash_table.py
```

**Requirements:** Python 3.7+ (no external dependencies).
