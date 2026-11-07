# Lab 12 - Hand Traces and Manual Verification

All traces use the campus graph in `graph.py` and the approved neighbour rule:
**process neighbours in ascending vertex-label order**.

Start vertices used: **ADM** (main run) and **GYM** (second required start).

---

## 1. BFS trace from ADM

BFS uses a FIFO queue. The queue column shows its contents **before** the
selected vertex is removed. Vertices are marked visited when they are
enqueued, so they never enter the queue twice. The visited set therefore grows when a
vertex is *discovered*, which is earlier than when it is *selected* (order).

| Step | Queue before pop | Selected | Newly discovered | Visited set after step (enqueue order) | Order after step |
|---:|---|---|---|---|---|
| 1 | ADM | ADM | ART, ENG, LIB, PARK | ADM, ART, ENG, LIB, PARK | ADM |
| 2 | ART, ENG, LIB, PARK | ART | - | ADM, ART, ENG, LIB, PARK | ADM, ART |
| 3 | ENG, LIB, PARK | ENG | GYM, SCI | ADM, ART, ENG, LIB, PARK, GYM, SCI | ADM, ART, ENG |
| 4 | LIB, PARK, GYM, SCI | LIB | CAF | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF | ADM, ART, ENG, LIB |
| 5 | PARK, GYM, SCI, CAF | PARK | - | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF | ADM, ART, ENG, LIB, PARK |
| 6 | GYM, SCI, CAF | GYM | DOR, MED | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED | ADM, ART, ENG, LIB, PARK, GYM |
| 7 | SCI, CAF, DOR, MED | SCI | - | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED | ADM, ART, ENG, LIB, PARK, GYM, SCI |
| 8 | CAF, DOR, MED | CAF | - | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF |
| 9 | DOR, MED | DOR | - | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR |
| 10 | MED | MED | - | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED | ADM, ART, ENG, LIB, PARK, GYM, SCI, CAF, DOR, MED |

**BFS order from ADM:**
`ADM -> ART -> ENG -> LIB -> PARK -> GYM -> SCI -> CAF -> DOR -> MED`

**BFS hop distances from ADM:**

| ADM | ART | ENG | LIB | PARK | GYM | SCI | CAF | DOR | MED | OBS |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 3 | unreachable |

**BFS parents (traversal tree):** ART<-ADM, ENG<-ADM, LIB<-ADM, PARK<-ADM,
GYM<-ENG, SCI<-ENG, CAF<-LIB, DOR<-GYM, MED<-GYM.

---

## 2. DFS trace from ADM (recursion / call stack)

The call stack is shown when a vertex is entered; the rightmost item is the
top of the stack. When a call returns, it is popped. Backtracking is implicit
in the recursion. DFS marks a vertex visited when its call is entered, so the
visited set always equals the order so far. Returns show up as a shrinking
stack between rows: after ART returns, the stack is back to ADM before ENG is
entered (step 3); after SCI returns, it unwinds to ADM, ENG, GYM, DOR before
MED is entered (step 9).

| Step | Call stack when entering | Selected | Visited set = order after step |
|---:|---|---|---|
| 1 | ADM | ADM | ADM |
| 2 | ADM, ART | ART | ADM, ART |
| 3 | ADM, ENG | ENG | ADM, ART, ENG |
| 4 | ADM, ENG, GYM | GYM | ADM, ART, ENG, GYM |
| 5 | ADM, ENG, GYM, DOR | DOR | ADM, ART, ENG, GYM, DOR |
| 6 | ADM, ENG, GYM, DOR, CAF | CAF | ADM, ART, ENG, GYM, DOR, CAF |
| 7 | ADM, ENG, GYM, DOR, CAF, LIB | LIB | ADM, ART, ENG, GYM, DOR, CAF, LIB |
| 8 | ADM, ENG, GYM, DOR, CAF, LIB, SCI | SCI | ADM, ART, ENG, GYM, DOR, CAF, LIB, SCI |
| 9 | ADM, ENG, GYM, DOR, MED | MED | ADM, ART, ENG, GYM, DOR, CAF, LIB, SCI, MED |
| 10 | ADM, PARK | PARK | ADM, ART, ENG, GYM, DOR, CAF, LIB, SCI, MED, PARK |

**DFS order from ADM:**
`ADM -> ART -> ENG -> GYM -> DOR -> CAF -> LIB -> SCI -> MED -> PARK`

The explicit-stack implementation (`dfs_iterative`) produces exactly the same
order and tree; both are checked in `test_graph.py` on the campus graph and on
random graphs.

---

## 3. Second starting vertex: GYM

### 3.1 BFS trace from GYM

| Step | Queue before pop | Selected | Newly discovered | Visited set after step (enqueue order) | Order after step |
|---:|---|---|---|---|---|
| 1 | GYM | GYM | DOR, ENG, MED, SCI | GYM, DOR, ENG, MED, SCI | GYM |
| 2 | DOR, ENG, MED, SCI | DOR | CAF | GYM, DOR, ENG, MED, SCI, CAF | GYM, DOR |
| 3 | ENG, MED, SCI, CAF | ENG | ADM | GYM, DOR, ENG, MED, SCI, CAF, ADM | GYM, DOR, ENG |
| 4 | MED, SCI, CAF, ADM | MED | - | GYM, DOR, ENG, MED, SCI, CAF, ADM | GYM, DOR, ENG, MED |
| 5 | SCI, CAF, ADM | SCI | LIB | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB | GYM, DOR, ENG, MED, SCI |
| 6 | CAF, ADM, LIB | CAF | - | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB | GYM, DOR, ENG, MED, SCI, CAF |
| 7 | ADM, LIB | ADM | ART, PARK | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART, PARK | GYM, DOR, ENG, MED, SCI, CAF, ADM |
| 8 | LIB, ART, PARK | LIB | - | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART, PARK | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB |
| 9 | ART, PARK | ART | - | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART, PARK | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART |
| 10 | PARK | PARK | - | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART, PARK | GYM, DOR, ENG, MED, SCI, CAF, ADM, LIB, ART, PARK |

BFS order: `GYM -> DOR -> ENG -> MED -> SCI -> CAF -> ADM -> LIB -> ART -> PARK`

BFS hops: ADM=2, ART=3, CAF=2, DOR=1, ENG=1, GYM=0, LIB=2, MED=1, PARK=3, SCI=1

### 3.2 DFS trace from GYM (call stack)

| Step | Call stack when entering | Selected | Visited set = order after step |
|---:|---|---|---|
| 1 | GYM | GYM | GYM |
| 2 | GYM, DOR | DOR | GYM, DOR |
| 3 | GYM, DOR, CAF | CAF | GYM, DOR, CAF |
| 4 | GYM, DOR, CAF, LIB | LIB | GYM, DOR, CAF, LIB |
| 5 | GYM, DOR, CAF, LIB, ADM | ADM | GYM, DOR, CAF, LIB, ADM |
| 6 | GYM, DOR, CAF, LIB, ADM, ART | ART | GYM, DOR, CAF, LIB, ADM, ART |
| 7 | GYM, DOR, CAF, LIB, ADM, ENG | ENG | GYM, DOR, CAF, LIB, ADM, ART, ENG |
| 8 | GYM, DOR, CAF, LIB, ADM, ENG, SCI | SCI | GYM, DOR, CAF, LIB, ADM, ART, ENG, SCI |
| 9 | GYM, DOR, CAF, LIB, ADM, PARK | PARK | GYM, DOR, CAF, LIB, ADM, ART, ENG, SCI, PARK |
| 10 | GYM, DOR, MED | MED | GYM, DOR, CAF, LIB, ADM, ART, ENG, SCI, PARK, MED |

DFS order: `GYM -> DOR -> CAF -> LIB -> ADM -> ART -> ENG -> SCI -> PARK -> MED`

DFS depth: ADM=4, ART=5, CAF=2, DOR=1, ENG=5, GYM=0, LIB=3, MED=2, PARK=5, SCI=6

The BFS and DFS orders differ, as expected, because one uses a queue and the
other a stack. Both visit every reachable vertex exactly once; `OBS` is never
reached.

---

## 4. Dijkstra settle trace from ADM

The priority queue always extracts the unsettled vertex with the smallest
tentative distance. When a vertex is settled its distance is final.

| Step | Selected | Distance | Neighbours updated |
|---:|---|---:|---|
| 1 | ADM | 0 | ART=4, ENG=2, LIB=2, PARK=1 |
| 2 | PARK | 1 | - |
| 3 | ENG | 2 | GYM=10, SCI=5 |
| 4 | LIB | 2 | CAF=8 |
| 5 | ART | 4 | - |
| 6 | SCI | 5 | CAF=7, GYM=9 |
| 7 | CAF | 7 | DOR=12 |
| 8 | GYM | 9 | MED=16 |
| 9 | DOR | 12 | MED=14 |
| 10 | MED | 14 | - |

`OBS` never enters the queue: it has no edges and is unreachable from ADM.

---

## 5. Routing table from ADM

| Target | Minutes | Hops | Reconstructed path |
|---|---:|---:|---|
| ART | 4 | 1 | ADM -> ART |
| CAF | 7 | 3 | ADM -> ENG -> SCI -> CAF |
| DOR | 12 | 4 | ADM -> ENG -> SCI -> CAF -> DOR |
| ENG | 2 | 1 | ADM -> ENG |
| GYM | 9 | 3 | ADM -> ENG -> SCI -> GYM |
| LIB | 2 | 1 | ADM -> LIB |
| MED | 14 | 5 | ADM -> ENG -> SCI -> CAF -> DOR -> MED |
| OBS | unreachable | - | - |
| PARK | 1 | 1 | ADM -> PARK |
| SCI | 5 | 2 | ADM -> ENG -> SCI |

---

## 6. Manual verification by summing edge weights

**Path 1 - ADM to MED (reported 14 minutes):**

```
ADM -> ENG -> SCI -> CAF -> DOR -> MED
  2  +   3  +   2  +   5  +   2   = 14   correct
```

There is an equal-cost alternative:

```
ADM -> LIB -> SCI -> CAF -> DOR -> MED
  2  +   3  +   2  +   5  +   2   = 14   equal cost
```

The BFS route is **not** the cheapest:

```
ADM -> ENG -> GYM -> MED
  2  +   8  +   7   = 17   more expensive
```

**Path 2 - ADM to GYM (reported 9 minutes):**

```
ADM -> ENG -> SCI -> GYM
  2  +   3  +   4   = 9    correct
```

Equal-cost alternative:

```
ADM -> LIB -> SCI -> GYM
  2  +   3  +   4   = 9    equal cost
```

The direct edge `ADM -> ENG -> GYM` would cost `2 + 8 = 10`, so the
reconstructed path is genuinely shorter.

---

## 7. BFS tree vs Dijkstra tree (Task D)

| Vertex | BFS hops | BFS path | Dijkstra minutes | Dijkstra path |
|---|---:|---|---:|---|
| ART | 1 | ADM -> ART | 4 | ADM -> ART |
| CAF | 2 | ADM -> LIB -> CAF | 7 | ADM -> ENG -> SCI -> CAF |
| DOR | 3 | ADM -> ENG -> GYM -> DOR | 12 | ADM -> ENG -> SCI -> CAF -> DOR |
| ENG | 1 | ADM -> ENG | 2 | ADM -> ENG |
| GYM | 2 | ADM -> ENG -> GYM | 9 | ADM -> ENG -> SCI -> GYM |
| LIB | 1 | ADM -> LIB | 2 | ADM -> LIB |
| MED | 3 | ADM -> ENG -> GYM -> MED | 14 | ADM -> ENG -> SCI -> CAF -> DOR -> MED |
| OBS | unreachable | - | unreachable | - |
| PARK | 1 | ADM -> PARK | 1 | ADM -> PARK |
| SCI | 2 | ADM -> ENG -> SCI | 5 | ADM -> ENG -> SCI |

The two trees agree for the nearest buildings but diverge for MED: BFS finds
the route with the fewest edges (3 hops, 17 minutes), while Dijkstra finds the
route with the least walking time (5 hops, 14 minutes).
