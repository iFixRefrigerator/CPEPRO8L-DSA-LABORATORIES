"""Evidence generator for Lab 12.

Run with:
    python demo.py

Prints the graph model, BFS/DFS traces, the Dijkstra routing table, the
BFS-tree vs shortest-path-tree comparison, and invalid-input handling.  The
same text is written to ``routing_results.txt`` for submission.
"""

from __future__ import annotations

from math import inf

from graph import (
    Graph,
    build_campus_graph,
    build_directed_demo_graph,
    build_unweighted_campus_graph,
)
from traversals import (
    bfs,
    bfs_trace,
    dfs_iterative,
    dfs_recursive,
    dfs_recursive_trace,
)
from dijkstra import all_shortest_paths, dijkstra, dijkstra_trace


class Reporter:
    def __init__(self):
        self.lines: list[str] = []

    def __call__(self, text: str = "") -> None:
        print(text)
        self.lines.append(text)

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(self.lines) + "\n")


def rule(title: str) -> str:
    return f"\n{title}\n{'-' * len(title)}"


def format_state(values) -> str:
    return "[" + ", ".join(values) + "]"


def main() -> None:
    out = Reporter()
    campus = build_campus_graph()

    out("LAB 12 - GRAPH TRAVERSALS AND SHORTEST-PATH ROUTING")
    out("=" * 57)
    out(f"Graph: {campus}")
    out("Neighbour-processing rule: ascending vertex label.")
    out("Weights are walking times in minutes (undirected campus graph).")

    # -------------------------------------------------------------------
    out(rule("1. EDGE TABLE"))
    out(f"{'edge':>12s}  {'minutes':>7s}")
    for u, v, w in campus.edges():
        out(f"{u + '-' + v:>12s}  {w:>7.1f}")

    # -------------------------------------------------------------------
    out(rule("2. ADJACENCY LIST"))
    for vertex in campus.vertices():
        entries = ", ".join(f"{v}({w:g})" for v, w in campus.adjacency(vertex))
        out(f"  {vertex:5s} -> {entries if entries else '(isolated)'}")

    # -------------------------------------------------------------------
    out(rule("3. BFS TRACE FROM ADM"))
    out("Queue is shown before the selected vertex is removed.")
    out(f"{'step':>4s}  {'queue before pop':<28s}  {'sel':<5s}  "
        f"{'discovered':<20s}  visited / order")
    for step in bfs_trace(campus, "ADM"):
        out(f"{step['step']:>4d}  {format_state(step['queue']):<28s}  "
            f"{step['selected']:<5s}  "
            f"{format_state(step['discovered']):<20s}  "
            f"{format_state(step['visited'])}")
    out(f"BFS order from ADM: {' -> '.join(bfs(campus, 'ADM').order)}")

    # -------------------------------------------------------------------
    out(rule("4. DFS TRACE FROM ADM (RECURSION / CALL STACK)"))
    out("The call stack is shown when a vertex is entered; rightmost is top.")
    out(f"{'step':>4s}  {'call stack':<34s}  {'sel':<5s}  order")
    for step in dfs_recursive_trace(campus, "ADM"):
        out(f"{step['step']:>4d}  {format_state(step['stack']):<34s}  "
            f"{step['selected']:<5s}  {format_state(step['order'])}")
    out(f"DFS order from ADM: {' -> '.join(dfs_recursive(campus, 'ADM').order)}")
    out("(The explicit-stack implementation produces the same order/tree; "
        "see section 6.)")

    # -------------------------------------------------------------------
    out(rule("5. SECOND STARTING VERTEX (GYM)"))
    bfs_gym = bfs(campus, "GYM")
    dfs_gym = dfs_recursive(campus, "GYM")
    out(f"BFS order from GYM: {' -> '.join(bfs_gym.order)}")
    out(f"BFS hops from GYM:  "
        + ", ".join(f"{v}={d}" for v, d in sorted(bfs_gym.distance.items())))
    out(f"DFS order from GYM: {' -> '.join(dfs_gym.order)}")
    out(f"DFS depth from GYM: "
        + ", ".join(f"{v}={d}" for v, d in sorted(dfs_gym.distance.items())))

    out(rule("6. RECURSIVE vs ITERATIVE DFS AGREEMENT"))
    for start in ("ADM", "GYM", "SCI", "OBS"):
        recursive = dfs_recursive(campus, start)
        iterative = dfs_iterative(campus, start)
        same = (recursive.order == iterative.order
                and recursive.parent == iterative.parent)
        out(f"  start={start:5s} same order/tree: {same}")

    # -------------------------------------------------------------------
    out(rule("7. DIJKSTRA SETTLE TRACE FROM ADM"))
    out(f"{'step':>4s}  {'sel':<5s}  {'dist':>6s}  updated neighbours")
    for step in dijkstra_trace(campus, "ADM"):
        updated = ", ".join(f"{v}={d:g}" for v, d in sorted(step["updated"].items()))
        out(f"{step['step']:>4d}  {step['selected']:<5s}  "
            f"{step['distance']:>6g}  {updated if updated else '-'}")

    # -------------------------------------------------------------------
    out(rule("8. ROUTING TABLE FROM ADM (WEIGHTED SHORTEST PATHS)"))
    result = dijkstra(campus, "ADM")
    out(f"{'target':<7s} {'minutes':>8s}  {'hops':>4s}  path")
    for target in campus.vertices():
        if target == "ADM":
            continue
        path = result.path_to(target)
        if path is None:
            out(f"{target:<7s} {'unreachable':>8s}  {'-':>4s}  -")
        else:
            out(f"{target:<7s} {result.dist[target]:>8g}  "
                f"{len(path) - 1:>4d}  {' -> '.join(path)}")

    out(rule("9. UNREACHABLE / ISOLATED VERTEX"))
    out(f"  unreachable from ADM: {result.unreachable()}")
    out("  OBS (Observatory) has no edges, so it cannot be routed to.")
    isolated = dijkstra(campus, "OBS")
    out(f"  dijkstra from OBS reaches only: {isolated.reachable()}")

    # -------------------------------------------------------------------
    out(rule("10. EQUAL-COST ALTERNATIVES"))
    for target in ("SCI", "CAF"):
        paths = all_shortest_paths(campus, "ADM", target)
        out(f"  ADM -> {target}: {len(paths)} equal-cost path(s)")
        for path, cost in paths:
            out(f"    cost {cost:g}: {' -> '.join(path)}")

    # -------------------------------------------------------------------
    out(rule("11. BFS TREE vs DIJKSTRA TREE FROM ADM"))
    out(f"{'vertex':<7s} {'BFS hops':>8s}  {'BFS path':<27s} "
        f"{'Dijkstra':>8s}  Dijkstra path")
    for target in campus.vertices():
        if target == "ADM":
            continue
        bfs_path = bfs(campus, "ADM").path_to(target)
        dj_path = result.path_to(target)
        hops = "-" if bfs_path is None else str(len(bfs_path) - 1)
        dj = "inf" if dj_path is None else f"{result.dist[target]:g}"
        bfs_text = "-" if bfs_path is None else " -> ".join(bfs_path)
        dj_text = "-" if dj_path is None else " -> ".join(dj_path)
        out(f"{target:<7s} {hops:>8s}  {bfs_text:<27s} {dj:>8s}  {dj_text}")
    out("Note: for MED, BFS uses 3 hops but Dijkstra uses 14 minutes via")
    out("      a different route.  Fewest edges is not fastest travel.")

    # -------------------------------------------------------------------
    out(rule("12. DIRECTED GRAPH SUPPORT"))
    directed = build_directed_demo_graph()
    out(f"Graph: {directed}")
    out(f"  ADM->LIB exists: {directed.has_edge('ADM', 'LIB')}; "
        f"LIB->ADM exists: {directed.has_edge('LIB', 'ADM')}")
    out(f"  BFS from ADM:   {' -> '.join(bfs(directed, 'ADM').order)}")
    directed_result = dijkstra(directed, "ADM")
    for target in directed.vertices():
        path = directed_result.path_to(target)
        shown = "unreachable" if path is None else " -> ".join(path)
        out(f"  {target:5s} {directed_result.dist[target]:>6g}  {shown}")

    # -------------------------------------------------------------------
    out(rule("13. INVALID-INPUT HANDLING EVIDENCE"))
    checks = []

    g1 = Graph(weighted=True)
    try:
        g1.add_edge("A", "B", -3)
    except ValueError as error:
        checks.append(("negative weight", str(error)))

    g2 = Graph(weighted=False)
    try:
        g2.add_edge("A", "B", 4)
    except ValueError as error:
        checks.append(("non-unit weight on unweighted graph", str(error)))

    g3 = Graph(weighted=True)
    g3.add_edge("A", "B", 1)
    try:
        g3.add_edge("A", "B", 2)
    except ValueError as error:
        checks.append(("duplicate edge", str(error)))

    for label, message in checks:
        out(f"  [{label}] rejected: {message}")

    out("  Dijkstra requires non-negative weights because it settles a")
    out("  vertex permanently once its distance is the smallest in the")
    out("  queue; a later negative edge could lower that settled distance,")
    out("  so the greedy assumption would be false.")

    out(rule("DONE"))
    out("Wrote routing_results.txt")
    out.save("routing_results.txt")


if __name__ == "__main__":
    main()
