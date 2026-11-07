"""Automated tests for Lab 12 - Graph Traversals and Shortest-Path Routing.

Run with:
    python -m unittest test_graph -v

The tests cover:
    * adjacency-list construction for directed/undirected and
      weighted/unweighted graphs;
    * deterministic BFS and DFS orders from two starting vertices;
    * recursive and explicit-stack DFS agreement;
    * Dijkstra distances, path reconstruction, unreachable/isolated vertices,
      equal-cost alternatives, and negative-weight rejection;
    * randomized cross-checks against independent reference implementations
      (Bellman-Ford for shortest paths, BFS for unit-weight distances).
"""

import math
import random
import unittest

from graph import (
    Graph,
    build_campus_graph,
    build_directed_demo_graph,
    build_unweighted_campus_graph,
    CAMPUS_EDGES,
    CAMPUS_VERTICES,
)
from traversals import bfs, bfs_path, dfs_iterative, dfs_recursive
from dijkstra import all_shortest_paths, dijkstra, shortest_path


def bellman_ford(graph, source):
    """Independent O(V*E) shortest-path reference (non-negative or not)."""
    dist = {v: math.inf for v in graph.vertices()}
    dist[source] = 0
    for _ in range(len(graph.vertices()) - 1):
        changed = False
        for u, v, w in graph.edges():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
            if not graph.directed and dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                changed = True
        if not changed:
            break
    return dist


def random_graph(rng, n, density, directed, weighted):
    """Build a random graph for property-based cross-checking."""
    labels = [f"V{i:02d}" for i in range(n)]
    graph = Graph(directed=directed, weighted=weighted)
    for label in labels:
        graph.add_vertex(label)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if not directed and j < i:
                continue
            if rng.random() < density:
                weight = rng.randint(0, 9) if weighted else 1
                if not graph.has_edge(labels[i], labels[j]):
                    graph.add_edge(labels[i], labels[j], weight)
    graph.validate()
    return graph, labels


class TestGraphModel(unittest.TestCase):
    def test_campus_vertices_and_edges(self):
        graph = build_campus_graph()
        self.assertTrue(graph.validate())
        self.assertEqual(graph.vertices(), sorted(CAMPUS_VERTICES))
        self.assertEqual(len(graph), 11)
        self.assertEqual(graph.edge_count(), len(CAMPUS_EDGES))
        self.assertEqual(graph.edge_count(), 14)
        for u, v, w in CAMPUS_EDGES:
            self.assertTrue(graph.has_edge(u, v), f"missing edge {u}-{v}")
            self.assertTrue(graph.has_edge(v, u), f"undirected edge {u}-{v} not symmetric")
            self.assertEqual(graph.edge_weight(u, v), float(w))

    def test_adjacency_lists_are_sorted(self):
        graph = build_campus_graph()
        expected = {
            "ADM": [("ART", 4.0), ("ENG", 2.0), ("LIB", 2.0), ("PARK", 1.0)],
            "SCI": [("CAF", 2.0), ("ENG", 3.0), ("GYM", 4.0), ("LIB", 3.0)],
            "MED": [("DOR", 2.0), ("GYM", 7.0)],
            "OBS": [],
        }
        for vertex, adjacency in expected.items():
            self.assertEqual(graph.adjacency(vertex), adjacency)
            self.assertEqual(graph.neighbors(vertex), [v for v, _ in adjacency])

    def test_undirected_symmetry(self):
        graph = build_campus_graph()
        for u, v, w in graph.edges():
            self.assertEqual(graph.edge_weight(v, u), w)

    def test_directed_edges_are_one_way(self):
        graph = build_directed_demo_graph()
        self.assertTrue(graph.directed)
        self.assertTrue(graph.has_edge("ADM", "LIB"))
        self.assertFalse(graph.has_edge("LIB", "ADM"))
        self.assertFalse(graph.has_edge("ADM", "GYM"))

    def test_unweighted_graph_uses_unit_weights(self):
        graph = build_unweighted_campus_graph()
        self.assertFalse(graph.weighted)
        self.assertTrue(all(w == 1 for _, _, w in graph.edges()))
        self.assertEqual(graph.edge_count(), len(CAMPUS_EDGES))

    def test_duplicate_and_invalid_edges_rejected(self):
        graph = Graph(directed=False, weighted=True)
        graph.add_edge("A", "B", 2)
        with self.assertRaises(ValueError):
            graph.add_edge("A", "B", 3)
        with self.assertRaises(ValueError):
            graph.add_edge("B", "A", 3)
        with self.assertRaises(ValueError):
            graph.add_edge("A", "C", -1)
        with self.assertRaises(ValueError):
            graph.add_edge("A", "D", "heavy")

    def test_unweighted_rejects_non_unit_weight(self):
        graph = Graph(weighted=False)
        with self.assertRaises(ValueError):
            graph.add_edge("A", "B", 5)

    def test_self_loop_is_handled(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_edge("A", "A", 0)
        self.assertEqual(graph.edge_weight("A", "A"), 0)
        self.assertEqual(graph.edge_count(), 1)
        self.assertTrue(graph.validate())

    def test_isolation_and_contains(self):
        graph = build_campus_graph()
        self.assertIn("OBS", graph)
        self.assertEqual(graph.neighbors("OBS"), [])
        self.assertNotIn("ZZZ", graph)


class TestTraversals(unittest.TestCase):
    EXPECTED_BFS_ADM = ["ADM", "ART", "ENG", "LIB", "PARK",
                        "GYM", "SCI", "CAF", "DOR", "MED"]
    EXPECTED_BFS_GYM = ["GYM", "DOR", "ENG", "MED", "SCI",
                        "CAF", "ADM", "LIB", "ART", "PARK"]
    EXPECTED_DFS_ADM = ["ADM", "ART", "ENG", "GYM", "DOR",
                        "CAF", "LIB", "SCI", "MED", "PARK"]
    EXPECTED_DFS_GYM = ["GYM", "DOR", "CAF", "LIB", "ADM",
                        "ART", "ENG", "SCI", "PARK", "MED"]

    def test_bfs_order_and_hops_from_adm(self):
        result = bfs(build_campus_graph(), "ADM")
        self.assertEqual(result.order, self.EXPECTED_BFS_ADM)
        expected_hops = {
            "ADM": 0, "ART": 1, "ENG": 1, "LIB": 1, "PARK": 1,
            "GYM": 2, "SCI": 2, "CAF": 2, "DOR": 3, "MED": 3,
        }
        self.assertEqual(result.distance, expected_hops)
        self.assertEqual(result.parent, {
            "ADM": None, "ART": "ADM", "ENG": "ADM", "LIB": "ADM",
            "PARK": "ADM", "GYM": "ENG", "SCI": "ENG", "CAF": "LIB",
            "DOR": "GYM", "MED": "GYM",
        })
        self.assertNotIn("OBS", result.order)

    def test_bfs_order_from_gym(self):
        result = bfs(build_campus_graph(), "GYM")
        self.assertEqual(result.order, self.EXPECTED_BFS_GYM)

    def test_dfs_order_from_adm(self):
        result = dfs_recursive(build_campus_graph(), "ADM")
        self.assertEqual(result.order, self.EXPECTED_DFS_ADM)
        self.assertEqual(result.parent, {
            "ADM": None, "ART": "ADM", "ENG": "ADM", "GYM": "ENG",
            "DOR": "GYM", "CAF": "DOR", "LIB": "CAF", "SCI": "LIB",
            "MED": "DOR", "PARK": "ADM",
        })

    def test_dfs_order_from_gym(self):
        result = dfs_recursive(build_campus_graph(), "GYM")
        self.assertEqual(result.order, self.EXPECTED_DFS_GYM)

    def test_dfs_iterative_matches_recursive_on_campus(self):
        graph = build_campus_graph()
        for start in ("ADM", "GYM", "SCI", "OBS"):
            recursive = dfs_recursive(graph, start)
            iterative = dfs_iterative(graph, start)
            self.assertEqual(recursive.order, iterative.order)
            self.assertEqual(recursive.parent, iterative.parent)
            self.assertEqual(recursive.distance, iterative.distance)

    def test_dfs_iterative_matches_recursive_on_random_graphs(self):
        rng = random.Random(2026)
        for directed in (False, True):
            for trial in range(12):
                graph, labels = random_graph(rng, 9, 0.30, directed, False)
                for start in (labels[0], labels[4]):
                    recursive = dfs_recursive(graph, start)
                    iterative = dfs_iterative(graph, start)
                    self.assertEqual(recursive.order, iterative.order,
                                     msg=f"directed={directed} trial={trial}")
                    self.assertEqual(recursive.parent, iterative.parent)

    def test_bfs_minimum_edge_path(self):
        graph = build_unweighted_campus_graph()
        path = bfs_path(graph, "ADM", "MED")
        self.assertEqual(path, ["ADM", "ENG", "GYM", "MED"])
        self.assertEqual(len(path) - 1, 3)

    def test_unknown_start_raises(self):
        graph = build_campus_graph()
        with self.assertRaises(ValueError):
            bfs(graph, "ZZZ")
        with self.assertRaises(ValueError):
            dfs_recursive(graph, "ZZZ")
        with self.assertRaises(ValueError):
            dfs_iterative(graph, "ZZZ")
        with self.assertRaises(ValueError):
            dijkstra(graph, "ZZZ")

    def test_traversals_do_not_modify_graph(self):
        graph = build_campus_graph()
        before = {v: graph.adjacency(v) for v in graph.vertices()}
        bfs(graph, "ADM")
        dfs_recursive(graph, "ADM")
        dfs_iterative(graph, "ADM")
        dijkstra(graph, "ADM")
        after = {v: graph.adjacency(v) for v in graph.vertices()}
        self.assertEqual(before, after)

    def test_cycle_visits_each_vertex_once(self):
        graph = Graph(weighted=True)
        cycle = ["A", "B", "C", "D", "E"]
        for i, vertex in enumerate(cycle):
            graph.add_edge(vertex, cycle[(i + 1) % len(cycle)], 1)
        for algorithm in (bfs, dfs_recursive, dfs_iterative):
            result = algorithm(graph, "A")
            self.assertEqual(len(result.order), len(set(result.order)))
            self.assertEqual(sorted(result.order), sorted(cycle))


class TestDijkstra(unittest.TestCase):
    EXPECTED_DIST = {
        "ADM": 0.0, "PARK": 1.0, "ENG": 2.0, "LIB": 2.0, "ART": 4.0,
        "SCI": 5.0, "CAF": 7.0, "GYM": 9.0, "DOR": 12.0, "MED": 14.0,
    }

    def test_distances_from_adm(self):
        graph = build_campus_graph()
        result = dijkstra(graph, "ADM")
        for target, expected in self.EXPECTED_DIST.items():
            self.assertAlmostEqual(result.dist[target], expected)
        self.assertEqual(result.dist["OBS"], math.inf)

    def test_settle_order_is_deterministic(self):
        result = dijkstra(build_campus_graph(), "ADM")
        self.assertEqual(
            result.settle_order,
            ["ADM", "PARK", "ENG", "LIB", "ART", "SCI", "CAF",
             "GYM", "DOR", "MED"],
        )

    def test_path_reconstruction(self):
        graph = build_campus_graph()
        result = dijkstra(graph, "ADM")
        expected_paths = {
            "PARK": ["ADM", "PARK"],
            "LIB": ["ADM", "LIB"],
            "ART": ["ADM", "ART"],
            "ENG": ["ADM", "ENG"],
            "SCI": ["ADM", "ENG", "SCI"],
            "CAF": ["ADM", "ENG", "SCI", "CAF"],
            "GYM": ["ADM", "ENG", "SCI", "GYM"],
            "DOR": ["ADM", "ENG", "SCI", "CAF", "DOR"],
            "MED": ["ADM", "ENG", "SCI", "CAF", "DOR", "MED"],
        }
        for target, expected in expected_paths.items():
            self.assertEqual(result.path_to(target), expected)

    def test_path_cost_equals_sum_of_weights(self):
        graph = build_campus_graph()
        result = dijkstra(graph, "ADM")
        for target in result.reachable():
            path = result.path_to(target)
            total = sum(graph.edge_weight(u, v) for u, v in zip(path, path[1:]))
            self.assertAlmostEqual(total, result.dist[target],
                                   msg=f"path cost mismatch for {target}")

    def test_manual_verification_two_paths(self):
        graph = build_campus_graph()
        # ADM -> MED manually: 2 + 3 + 2 + 5 + 2 = 14
        distance, path = shortest_path(graph, "ADM", "MED")
        self.assertEqual(path, ["ADM", "ENG", "SCI", "CAF", "DOR", "MED"])
        self.assertEqual(distance, 14)
        # ADM -> GYM manually: 2 + 3 + 4 = 9
        distance, path = shortest_path(graph, "ADM", "GYM")
        self.assertEqual(path, ["ADM", "ENG", "SCI", "GYM"])
        self.assertEqual(distance, 9)

    def test_unreachable_and_isolated_vertex(self):
        graph = build_campus_graph()
        result = dijkstra(graph, "ADM")
        self.assertFalse(result.is_reachable("OBS"))
        self.assertIsNone(result.path_to("OBS"))
        self.assertEqual(result.dist["OBS"], math.inf)
        self.assertEqual(result.unreachable(), ["OBS"])

    def test_isolated_source(self):
        graph = build_campus_graph()
        result = dijkstra(graph, "OBS")
        self.assertEqual(result.reachable(), ["OBS"])
        self.assertEqual(result.dist["OBS"], 0)
        self.assertEqual(len(result.unreachable()), 10)
        self.assertEqual(result.path_to("ADM"), None)

    def test_equal_cost_alternatives(self):
        graph = build_campus_graph()
        paths = all_shortest_paths(graph, "ADM", "SCI")
        self.assertEqual(len(paths), 2)
        self.assertEqual({tuple(p) for p, _ in paths}, {
            ("ADM", "ENG", "SCI"),
            ("ADM", "LIB", "SCI"),
        })
        self.assertTrue(all(cost == 5 for _, cost in paths))

    def test_no_path_returns_empty_alternatives(self):
        self.assertEqual(all_shortest_paths(build_campus_graph(), "ADM", "OBS"), [])

    def test_negative_weight_rejected_by_dijkstra(self):
        graph = Graph(directed=True, weighted=True)
        graph.add_edge("A", "B", 1)
        graph.add_edge("B", "C", 1)
        # Bypass add_edge to simulate corrupted input loaded from a file.
        graph._adj["A"] = [("B", -5)]
        graph._edges[("A", "B")] = -5
        with self.assertRaises(ValueError):
            dijkstra(graph, "A")

    def test_unit_weight_dijkstra_equals_bfs_hops(self):
        graph = build_unweighted_campus_graph()
        result = dijkstra(graph, "ADM")
        traversal = bfs(graph, "ADM")
        for vertex in graph.vertices():
            if vertex == "OBS":
                self.assertEqual(result.dist[vertex], math.inf)
            else:
                self.assertEqual(result.dist[vertex], traversal.distance[vertex])

    def test_bfs_tree_differs_from_weighted_tree(self):
        """Task D: minimum hops is not the same as minimum walking time."""
        graph = build_campus_graph()
        bfs_result = bfs(graph, "ADM")
        dijkstra_result = dijkstra(graph, "ADM")
        self.assertEqual(bfs_result.distance["MED"], 3)          # hops
        self.assertEqual(dijkstra_result.dist["MED"], 14)        # minutes
        self.assertEqual(bfs_result.path_to("MED"), ["ADM", "ENG", "GYM", "MED"])
        self.assertEqual(dijkstra_result.path_to("MED"),
                         ["ADM", "ENG", "SCI", "CAF", "DOR", "MED"])

    def test_dijkstra_matches_bellman_ford_on_random_graphs(self):
        rng = random.Random(99)
        for directed in (False, True):
            for weighted in (False, True):
                for trial in range(8):
                    graph, labels = random_graph(
                        rng, 10, 0.25, directed, weighted
                    )
                    source = labels[0]
                    expected = bellman_ford(graph, source)
                    observed = dijkstra(graph, source).dist
                    for vertex in graph.vertices():
                        self.assertEqual(
                            observed[vertex] == math.inf,
                            expected[vertex] == math.inf,
                            msg=f"reachability mismatch {directed=} {weighted=} "
                                f"trial={trial} vertex={vertex}",
                        )
                        if expected[vertex] != math.inf:
                            self.assertAlmostEqual(observed[vertex],
                                                   expected[vertex])

    def test_directed_graph_distances(self):
        graph = build_directed_demo_graph()
        result = dijkstra(graph, "ADM")
        self.assertEqual(result.dist, {
            "ADM": 0.0, "ENG": 2.0, "GYM": 4.0, "LIB": 1.0, "SCI": 3.0,
        })


if __name__ == "__main__":
    unittest.main(verbosity=2)
