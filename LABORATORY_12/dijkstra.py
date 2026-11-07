"""Dijkstra's single-source shortest-path algorithm for Lab 12.

Uses ``heapq`` as the priority queue, stores tentative distances and
predecessors, and reconstructs paths.  A stale-entry ("lazy deletion")
approach is used instead of a decrease-key operation: a heap entry is
ignored when it is older than the best known distance.

Complexity with an adjacency list and a binary heap:
    time  O((V + E) log V)      (O(E log V) in practice)
    space O(V + E) for the graph and O(V) for the result

Negative edge weights are rejected because Dijkstra assumes that once a
vertex is settled its distance can never improve; a negative edge could
lower an already-settled distance and invalidate the result.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import inf

from graph import Graph


@dataclass
class DijkstraResult:
    """Shortest-path result from one source.

    ``dist[v]`` is the shortest distance (``inf`` if unreachable) and
    ``prev[v]`` is the predecessor on the chosen shortest path (``None`` for
    the source and for unreachable vertices).
    """

    source: str
    dist: dict[str, float]
    prev: dict[str, str | None]
    settle_order: list[str]

    def is_reachable(self, target: str) -> bool:
        if target not in self.dist:
            raise KeyError(f"vertex {target!r} is not in the graph")
        return self.dist[target] < inf

    def path_to(self, target: str) -> list[str] | None:
        """Reconstruct the shortest path, or ``None`` if unreachable."""
        if target not in self.dist:
            raise KeyError(f"vertex {target!r} is not in the graph")
        if self.dist[target] == inf:
            return None
        path: list[str] = []
        current: str | None = target
        while current is not None:
            path.append(current)
            current = self.prev[current]
        path.reverse()
        return path

    def distance_to(self, target: str) -> float:
        if target not in self.dist:
            raise KeyError(f"vertex {target!r} is not in the graph")
        return self.dist[target]

    def reachable(self) -> list[str]:
        return sorted(v for v, d in self.dist.items() if d < inf)

    def unreachable(self) -> list[str]:
        return sorted(v for v, d in self.dist.items() if d == inf)


def _reject_negative_weights(graph: Graph) -> None:
    for u, v, w in graph.edges():
        if w < 0:
            raise ValueError(
                f"negative edge weight {w!r} on {u!r}-{v!r}: Dijkstra's "
                "algorithm is invalid for negative weights"
            )


def dijkstra(graph: Graph, source: str) -> DijkstraResult:
    """Run Dijkstra from ``source`` and return distances/predecessors."""
    if not graph.has_vertex(source):
        raise ValueError(f"source vertex {source!r} is not in the graph")
    _reject_negative_weights(graph)

    dist: dict[str, float] = {v: inf for v in graph.vertices()}
    prev: dict[str, str | None] = {v: None for v in graph.vertices()}
    dist[source] = 0
    settle_order: list[str] = []
    settled: set[str] = set()

    counter = 0
    heap: list[tuple[float, int, str]] = [(0.0, counter, source)]

    while heap:
        d, _, u = heapq.heappop(heap)
        if u in settled or d > dist[u]:
            continue          # stale heap entry from lazy deletion
        settled.add(u)
        settle_order.append(u)
        for v, w in graph.adjacency(u):
            candidate = d + w
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                counter += 1
                heapq.heappush(heap, (candidate, counter, v))

    return DijkstraResult(source, dist, prev, settle_order)


def shortest_path(graph: Graph, source: str, target: str):
    """Return ``(distance, path)``; path is ``None`` if unreachable."""
    result = dijkstra(graph, source)
    return result.dist[target], result.path_to(target)


def all_shortest_paths(graph: Graph, source: str, target: str):
    """Return every minimum-cost path as ``[(path, cost), ...]``.

    Only edges that lie on a shortest path are followed (tight edges where
    ``dist[u] + w == dist[v]``).  Results are sorted deterministically.
    """
    result = dijkstra(graph, source)
    if not result.is_reachable(target):
        return []

    paths: list[tuple[list[str], float]] = []
    path = [source]
    in_path = {source}

    def walk(u: str) -> None:
        if u == target:
            paths.append((list(path), result.dist[target]))
            return
        for v, w in graph.adjacency(u):
            if result.dist[v] < inf and result.dist[u] + w == result.dist[v]:
                if v not in in_path:      # guard against zero-weight cycles
                    path.append(v)
                    in_path.add(v)
                    walk(v)
                    in_path.remove(v)
                    path.pop()

    walk(source)
    paths.sort(key=lambda item: (item[1], item[0]))
    return paths


def dijkstra_trace(graph: Graph, source: str) -> list[dict]:
    """Return step-by-step settled-vertex state for hand-trace evidence."""
    if not graph.has_vertex(source):
        raise ValueError(f"source vertex {source!r} is not in the graph")
    _reject_negative_weights(graph)

    dist: dict[str, float] = {v: inf for v in graph.vertices()}
    prev: dict[str, str | None] = {v: None for v in graph.vertices()}
    dist[source] = 0
    settled: set[str] = set()
    counter = 0
    heap: list[tuple[float, int, str]] = [(0.0, counter, source)]
    steps: list[dict] = []
    step = 0

    while heap:
        d, _, u = heapq.heappop(heap)
        if u in settled or d > dist[u]:
            continue
        settled.add(u)
        step += 1
        updated = {}
        for v, w in graph.adjacency(u):
            candidate = d + w
            if candidate < dist[v]:
                dist[v] = candidate
                prev[v] = u
                counter += 1
                heapq.heappush(heap, (candidate, counter, v))
                updated[v] = candidate
        steps.append(
            dict(
                step=step,
                selected=u,
                distance=d,
                updated=updated,
                settled=sorted(settled),
            )
        )

    return steps


if __name__ == "__main__":
    from graph import build_campus_graph

    campus = build_campus_graph()
    result = dijkstra(campus, "ADM")
    print(f"Shortest distances from ADM ({result.source}):")
    for target in campus.vertices():
        distance = result.dist[target]
        path = result.path_to(target)
        shown = "unreachable" if path is None else " -> ".join(path)
        print(f"  {target:5s} {distance:6.1f}  {shown}")
