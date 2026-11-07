"""Breadth-First Search and Depth-First Search for Lab 12.

Both traversals use the graph's deterministic neighbour order (ascending
vertex label), so their results are reproducible.

BFS uses a FIFO queue (``collections.deque``).  DFS is provided twice:
a recursive version and an explicit-stack version.  Both must produce the
same preorder sequence and the same traversal tree; a unit test checks that.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from graph import Graph, build_campus_graph


@dataclass
class TraversalResult:
    """Result of one traversal.

    ``distance`` means number of edges from ``start`` (BFS hops) or recursion
    depth (DFS).  ``parent`` defines the traversal tree; the start maps to
    ``None``.  Only reached vertices appear in ``parent`` and ``distance``.
    """

    start: str
    order: list[str]
    parent: dict[str, str | None]
    distance: dict[str, int]

    def path_to(self, target: str) -> list[str] | None:
        """Reconstruct the traversal-tree path from ``start`` to ``target``."""
        if target not in self.parent:
            return None
        path = []
        current: str | None = target
        while current is not None:
            path.append(current)
            current = self.parent[current]
        path.reverse()
        return path

    def reached(self) -> list[str]:
        """Vertices reached by the traversal, in ascending order."""
        return sorted(self.parent)


def _require_vertex(graph: Graph, vertex: str) -> None:
    if not graph.has_vertex(vertex):
        raise ValueError(f"start vertex {vertex!r} is not in the graph")


def bfs(graph: Graph, start: str) -> TraversalResult:
    """Breadth-First Search using a queue and a visited set.

    Time O(V + E), space O(V).
    """
    _require_vertex(graph, start)
    order: list[str] = []
    parent: dict[str, str | None] = {start: None}
    distance: dict[str, int] = {start: 0}
    visited = {start}
    queue: deque[str] = deque([start])

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                distance[v] = distance[u] + 1
                queue.append(v)

    return TraversalResult(start, order, parent, distance)


def bfs_trace(graph: Graph, start: str) -> list[dict]:
    """Return step-by-step BFS state for hand-trace evidence.

    Each step records the queue contents *before* the selected vertex is
    removed, the selected vertex, newly discovered neighbours, the visited
    set, and the traversal order so far.
    """
    _require_vertex(graph, start)
    steps: list[dict] = []
    order: list[str] = []
    parent: dict[str, str | None] = {start: None}
    distance: dict[str, int] = {start: 0}
    visited = {start}
    queue: deque[str] = deque([start])
    step = 0

    while queue:
        snapshot = list(queue)
        u = queue.popleft()
        order.append(u)
        step += 1
        discovered = []
        for v in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                parent[v] = u
                distance[v] = distance[u] + 1
                queue.append(v)
                discovered.append(v)
        steps.append(
            dict(
                step=step,
                queue=snapshot,
                selected=u,
                discovered=discovered,
                visited=sorted(visited),
                order=list(order),
            )
        )

    return steps


def dfs_recursive(graph: Graph, start: str) -> TraversalResult:
    """Depth-First Search using recursion.

    Time O(V + E), space O(V) (call stack).
    """
    _require_vertex(graph, start)
    order: list[str] = []
    parent: dict[str, str | None] = {start: None}
    depth: dict[str, int] = {start: 0}
    visited: set[str] = set()

    def visit(u: str) -> None:
        visited.add(u)
        order.append(u)
        for v in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                depth[v] = depth[u] + 1
                visit(v)

    visit(start)
    return TraversalResult(start, order, parent, depth)


def dfs_iterative(graph: Graph, start: str) -> TraversalResult:
    """Depth-First Search using an explicit stack.

    Neighbours are pushed in reverse order so the ascending-order neighbour is
    popped first, matching :func:`dfs_recursive` exactly.  A vertex is marked
    visited when popped, and its parent is taken from the stack entry, which
    reproduces the recursive traversal tree.

    Time O(V + E), space O(V).
    """
    _require_vertex(graph, start)
    order: list[str] = []
    parent: dict[str, str | None] = {}
    depth: dict[str, int] = {}
    visited: set[str] = set()
    stack: list[tuple[str, str | None]] = [(start, None)]

    while stack:
        u, p = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        parent[u] = p
        depth[u] = 0 if p is None else depth[p] + 1
        order.append(u)
        for v in reversed(graph.neighbors(u)):
            if v not in visited:
                stack.append((v, u))

    return TraversalResult(start, order, parent, depth)


def dfs_trace(graph: Graph, start: str) -> list[dict]:
    """Return step-by-step explicit-stack DFS state for hand-trace evidence."""
    _require_vertex(graph, start)
    steps: list[dict] = []
    order: list[str] = []
    visited: set[str] = set()
    stack: list[tuple[str, str | None]] = [(start, None)]
    step = 0

    while stack:
        snapshot = [v for v, _ in stack]
        u, p = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        step += 1
        pushed = []
        for v in reversed(graph.neighbors(u)):
            if v not in visited:
                stack.append((v, u))
                pushed.append(v)
        pushed.reverse()
        steps.append(
            dict(
                step=step,
                stack=snapshot,
                selected=u,
                pushed=pushed,
                visited=sorted(visited),
                order=list(order),
            )
        )

    return steps


def bfs_path(graph: Graph, start: str, target: str) -> list[str] | None:
    """Minimum-edge path from ``start`` to ``target`` (unweighted optimal)."""
    return bfs(graph, start).path_to(target)


def dfs_recursive_trace(graph: Graph, start: str) -> list[dict]:
    """Step-by-step recursive DFS state, showing the call stack as the stack."""
    _require_vertex(graph, start)
    steps: list[dict] = []
    order: list[str] = []
    visited: set[str] = set()
    call_stack: list[str] = []
    step = 0

    def visit(u: str) -> None:
        nonlocal step
        step += 1
        visited.add(u)
        order.append(u)
        call_stack.append(u)
        steps.append(
            dict(
                step=step,
                stack=list(call_stack),
                selected=u,
                visited=sorted(visited),
                order=list(order),
            )
        )
        for v in graph.neighbors(u):
            if v not in visited:
                visit(v)
        call_stack.pop()

    visit(start)
    return steps


def dfs_path(graph: Graph, start: str, target: str) -> list[str] | None:
    """Path found by DFS (not guaranteed to be shortest)."""
    return dfs_recursive(graph, start).path_to(target)


if __name__ == "__main__":
    campus = build_campus_graph()
    for source in ("ADM", "GYM"):
        result = bfs(campus, source)
        print(f"BFS  from {source}: {' -> '.join(result.order)}")
        print(f"     hops: {result.distance}")
        result = dfs_recursive(campus, source)
        print(f"DFS  from {source}: {' -> '.join(result.order)}")
        print(f"     depth: {result.distance}")
