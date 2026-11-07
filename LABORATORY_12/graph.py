"""Adjacency-list graph model for Lab 12 - Graph Traversals and Shortest Paths.

The module supports four combinations of graph type:
    - undirected / directed
    - unweighted / weighted

Design notes
------------
* The adjacency list is stored as ``vertex -> [(neighbor, weight), ...]``.
* Neighbours are always kept in sorted (ascending) order, so BFS and DFS
  produce a deterministic traversal order.  This is the ordering rule used
  throughout the lab: process neighbours by ascending vertex label.
* Unweighted graphs store a weight of ``1`` for every edge.  Inserting a
  non-unit weight into an unweighted graph is rejected.
* Negative weights are rejected at insertion time for weighted graphs,
  because Dijkstra's algorithm requires non-negative edge weights.
* The input graph is never modified by the traversal or routing modules.

Campus routing dataset
----------------------
No instructor-supplied dataset was attached to the laboratory handout, so a
representative campus walking-time graph is encoded here.  Replace the edge
table in :data:`CAMPUS_EDGES` with the assigned dataset if the instructor
provides one; the algorithms and tests do not depend on these particular
labels.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Campus routing dataset (undirected, walking time in minutes)
# ---------------------------------------------------------------------------

CAMPUS_VERTICES = [
    "ADM",   # Administration
    "ART",   # Arts Building
    "CAF",   # Cafeteria
    "DOR",   # Dormitory
    "ENG",   # Engineering
    "GYM",   # Gymnasium
    "LIB",   # Library
    "MED",   # Medical Clinic
    "OBS",   # Observatory (isolated: no paths connect it to campus)
    "PARK",  # Parking Lot
    "SCI",   # Science Building
]

# (u, v, walking_minutes)
CAMPUS_EDGES = [
    ("ADM", "LIB", 2),
    ("ADM", "ENG", 2),
    ("LIB", "SCI", 3),
    ("ENG", "SCI", 3),
    ("LIB", "CAF", 6),
    ("SCI", "CAF", 2),
    ("CAF", "DOR", 5),
    ("ENG", "GYM", 8),
    ("SCI", "GYM", 4),
    ("GYM", "DOR", 6),
    ("GYM", "MED", 7),
    ("DOR", "MED", 2),
    ("ADM", "ART", 4),
    ("ADM", "PARK", 1),
]


# One-way road example used to prove that directed graphs are supported.
DIRECTED_DEMO_VERTICES = ["ADM", "ENG", "GYM", "LIB", "SCI"]
DIRECTED_DEMO_EDGES = [
    ("ADM", "LIB", 1),
    ("LIB", "ENG", 1),
    ("ENG", "SCI", 1),
    ("SCI", "GYM", 1),
    ("GYM", "ADM", 1),   # closes a one-way cycle
    ("ADM", "ENG", 2),   # directed shortcut
]


# ---------------------------------------------------------------------------
# Graph class
# ---------------------------------------------------------------------------

class Graph:
    """An adjacency-list graph.

    Parameters
    ----------
    directed:
        ``True`` for a directed graph, ``False`` for undirected (default).
    weighted:
        ``True`` to store edge weights, ``False`` for a unit-weight graph.
    """

    def __init__(self, directed: bool = False, weighted: bool = False):
        self.directed = directed
        self.weighted = weighted
        self._adj: dict[str, list[tuple[str, float]]] = {}
        self._edges: dict[tuple[str, str], float] = {}

    # -- internal helpers ---------------------------------------------------

    def _key(self, u: str, v: str) -> tuple[str, str]:
        """Canonical edge key (undirected edges are unordered)."""
        if self.directed:
            return (u, v)
        return (u, v) if u <= v else (v, u)

    def _check_weight(self, weight) -> float:
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError(f"edge weight must be numeric, got {weight!r}")
        if weight < 0:
            raise ValueError(
                f"negative edge weight {weight!r} rejected: Dijkstra requires "
                "non-negative weights"
            )
        if not self.weighted and weight != 1:
            raise ValueError(
                "unweighted graphs only accept unit weights (weight=1)"
            )
        return float(weight)

    def _insert(self, u: str, v: str, weight: float) -> None:
        self._adj.setdefault(u, []).append((v, weight))
        self._adj[u].sort(key=lambda item: item[0])

    # -- construction -------------------------------------------------------

    def add_vertex(self, vertex: str) -> None:
        """Add an isolated vertex if it is not already present."""
        if not isinstance(vertex, str) or vertex == "":
            raise ValueError("vertex labels must be non-empty strings")
        self._adj.setdefault(vertex, [])

    def add_edge(self, u: str, v: str, weight: float = 1) -> None:
        """Add an edge (and its endpoints, if missing).

        Raises ``ValueError`` for a duplicate edge, an invalid weight, or a
        negative weight.
        """
        weight = self._check_weight(weight)
        key = self._key(u, v)
        if key in self._edges:
            raise ValueError(f"duplicate edge {u!r}-{v!r}")
        self.add_vertex(u)
        self.add_vertex(v)
        self._edges[key] = weight
        self._insert(u, v, weight)
        if not self.directed and u != v:
            self._insert(v, u, weight)

    # -- queries ------------------------------------------------------------

    def has_vertex(self, vertex: str) -> bool:
        return vertex in self._adj

    def has_edge(self, u: str, v: str) -> bool:
        return self._key(u, v) in self._edges

    def vertices(self) -> list[str]:
        """All vertex labels in ascending order."""
        return sorted(self._adj)

    def neighbors(self, vertex: str) -> list[str]:
        """Neighbour labels in ascending order (deterministic rule)."""
        return [v for v, _ in self._adj[vertex]]

    def adjacency(self, vertex: str) -> list[tuple[str, float]]:
        """(neighbour, weight) pairs in ascending neighbour order."""
        return list(self._adj[vertex])

    def edge_weight(self, u: str, v: str) -> float:
        key = self._key(u, v)
        if key not in self._edges:
            raise KeyError(f"no edge {u!r}-{v!r}")
        return self._edges[key]

    def edges(self) -> list[tuple[str, str, float]]:
        """Unique edges as ``(u, v, weight)``, sorted for reproducibility.

        Undirected edges appear once, using the ascending label order.
        """
        out = []
        seen = set()
        for u in self.vertices():
            for v, w in self.adjacency(u):
                key = self._key(u, v)
                if key in seen:
                    continue
                seen.add(key)
                out.append((key[0], key[1], w))
        return sorted(out)

    def edge_count(self) -> int:
        return len(self._edges)

    # -- validation ---------------------------------------------------------

    def validate(self) -> bool:
        """Check internal consistency; raise ``ValueError`` on any problem."""
        for u, entries in self._adj.items():
            if not isinstance(u, str):
                raise ValueError(f"invalid vertex label {u!r}")
            seen_neighbors = set()
            for v, w in entries:
                if v not in self._adj:
                    raise ValueError(f"missing vertex {v!r} referenced by {u!r}")
                if v in seen_neighbors:
                    raise ValueError(f"duplicate neighbor {v!r} of {u!r}")
                seen_neighbors.add(v)
                if w < 0:
                    raise ValueError(f"negative weight on edge {u!r}-{v!r}")
                if not self.weighted and w != 1:
                    raise ValueError(f"non-unit weight on unweighted edge {u!r}-{v!r}")
                if not self.directed:
                    if not self.has_edge(v, u):
                        raise ValueError(f"missing reverse edge {v!r}-{u!r}")
                    if self.edge_weight(v, u) != w:
                        raise ValueError(f"asymmetric weights on {u!r}-{v!r}")
        return True

    # -- dunder helpers -----------------------------------------------------

    def __len__(self) -> int:
        return len(self._adj)

    def __iter__(self):
        return iter(self.vertices())

    def __contains__(self, vertex: str) -> bool:
        return self.has_vertex(vertex)

    def __repr__(self) -> str:
        kind = "directed" if self.directed else "undirected"
        weights = "weighted" if self.weighted else "unweighted"
        return (f"Graph({kind}, {weights}, "
                f"vertices={len(self._adj)}, edges={self.edge_count()})")


# ---------------------------------------------------------------------------
# Dataset builders
# ---------------------------------------------------------------------------

def build_campus_graph() -> Graph:
    """Weighted, undirected campus walking-time graph."""
    g = Graph(directed=False, weighted=True)
    for vertex in CAMPUS_VERTICES:
        g.add_vertex(vertex)
    for u, v, minutes in CAMPUS_EDGES:
        g.add_edge(u, v, minutes)
    g.validate()
    return g


def build_unweighted_campus_graph() -> Graph:
    """Same topology as the campus graph, but every edge has unit weight."""
    g = Graph(directed=False, weighted=False)
    for vertex in CAMPUS_VERTICES:
        g.add_vertex(vertex)
    for u, v, _minutes in CAMPUS_EDGES:
        g.add_edge(u, v)
    g.validate()
    return g


def build_directed_demo_graph() -> Graph:
    """Directed, weighted example with a one-way cycle and a shortcut."""
    g = Graph(directed=True, weighted=True)
    for vertex in DIRECTED_DEMO_VERTICES:
        g.add_vertex(vertex)
    for u, v, weight in DIRECTED_DEMO_EDGES:
        g.add_edge(u, v, weight)
    g.validate()
    return g


def campus_edge_table() -> list[tuple[str, str, int]]:
    """Return the campus edge table sorted by endpoint labels."""
    return sorted(CAMPUS_EDGES)


if __name__ == "__main__":
    graph = build_campus_graph()
    print(graph)
    print(f"{'edge':>12s}  {'minutes':>7s}")
    for u, v, w in graph.edges():
        print(f"{u + '-' + v:>12s}  {w:>7.1f}")
