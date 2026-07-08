"""Experiment pipeline for the routing algorithm comparison."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable

from routing_project.algorithms import AlgorithmResult, astar, bellman_ford, dijkstra, harmony_search
from routing_project.graph import WeightedGraph, generate_connected_graph


CSV_FIELDS = [
    "algorithm",
    "graph_id",
    "nodes",
    "edges",
    "density",
    "source",
    "target",
    "path_cost",
    "runtime_ms",
    "success",
    "seed",
    "hmcr",
    "par",
    "hms",
    "iterations",
]


@dataclass(frozen=True)
class ExperimentConfig:
    node_counts: tuple[int, ...]
    densities: tuple[str, ...]
    graph_seeds: tuple[int, ...]
    deterministic_repeats: int = 3
    harmony_trials: int = 5
    harmony_iterations: int = 150
    hmcr: float = 0.8
    par: float = 0.3
    hms: int = 30


SMALL_CONFIG = ExperimentConfig(
    node_counts=(20, 50),
    densities=("sparse", "moderate"),
    graph_seeds=(11, 23),
    deterministic_repeats=2,
    harmony_trials=3,
    harmony_iterations=80,
)


CHECKPOINT_CONFIG = ExperimentConfig(
    node_counts=(50, 250, 1000),
    densities=("sparse", "moderate", "dense"),
    graph_seeds=(11, 23, 37),
    deterministic_repeats=5,
    harmony_trials=30,
    harmony_iterations=250,
)


def run_experiment(config: ExperimentConfig, output_csv: Path) -> list[dict[str, object]]:
    """Run the configured experiment grid and write normalized CSV rows."""

    rows: list[dict[str, object]] = []
    for node_count in config.node_counts:
        for density in config.densities:
            for graph_seed in config.graph_seeds:
                graph = generate_connected_graph(node_count, density=density, seed=graph_seed)
                graph_id = f"v{node_count}_{density}_seed{graph_seed}"
                source, target = 0, node_count - 1
                rows.extend(
                    _run_graph_trials(
                        graph,
                        graph_id,
                        density,
                        source,
                        target,
                        config,
                        graph_seed,
                    )
                )

    write_rows(output_csv, rows)
    return rows


def run_parameter_sweep(
    output_csv: Path,
    node_count: int = 500,
    trials: int = 3,
    iterations: int = 100,
    progress: bool = False,
) -> list[dict[str, object]]:
    """Run the Harmony Search parameter sweep from the checkpoint-one plan."""

    graph = generate_connected_graph(node_count, density="moderate", seed=101)
    source, target = 0, node_count - 1
    rows: list[dict[str, object]] = []
    for hmcr in (0.7, 0.8, 0.9):
        for par in (0.1, 0.3, 0.5):
            for hms in (10, 30, 50):
                if progress:
                    print(f"Sweeping HMCR={hmcr}, PAR={par}, HMS={hms}")
                for trial in range(trials):
                    result = harmony_search(
                        graph,
                        source,
                        target,
                        hmcr=hmcr,
                        par=par,
                        hms=hms,
                        iterations=iterations,
                        seed=10_000 + trial,
                    )
                    rows.append(
                        result_to_row(
                            result,
                            graph,
                            f"v{node_count}_moderate_seed101",
                            "moderate",
                            source,
                            target,
                        )
                    )
    write_rows(output_csv, rows)
    return rows


def write_rows(output_csv: Path, rows: Iterable[dict[str, object]]) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CSV_FIELDS})


def result_to_row(
    result: AlgorithmResult,
    graph: WeightedGraph,
    graph_id: str,
    density: str,
    source: int,
    target: int,
) -> dict[str, object]:
    return {
        "algorithm": result.algorithm,
        "graph_id": graph_id,
        "nodes": len(graph.nodes()),
        "edges": graph.edge_count(),
        "density": density,
        "source": source,
        "target": target,
        "path_cost": round(result.cost, 6) if result.success else "",
        "runtime_ms": round(result.runtime_ms, 6),
        "success": result.success,
        "seed": result.metadata.get("seed", ""),
        "hmcr": result.metadata.get("hmcr", ""),
        "par": result.metadata.get("par", ""),
        "hms": result.metadata.get("hms", ""),
        "iterations": result.metadata.get("iterations", ""),
    }


def summarize_by_algorithm(rows: Iterable[dict[str, object]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(str(row["algorithm"]), []).append(row)
    summary: dict[str, dict[str, float]] = {}
    for algorithm, items in grouped.items():
        runtimes = [float(item["runtime_ms"]) for item in items if item["runtime_ms"] != ""]
        costs = [float(item["path_cost"]) for item in items if item["path_cost"] != ""]
        summary[algorithm] = {
            "mean_runtime_ms": mean(runtimes) if runtimes else 0.0,
            "mean_path_cost": mean(costs) if costs else 0.0,
            "success_rate": sum(str(item["success"]) == "True" for item in items) / len(items),
        }
    return summary


def format_result_summary(rows: Iterable[dict[str, object]]) -> str:
    """Build a short human-readable interpretation of experiment rows."""

    row_list = list(rows)
    summary = summarize_by_algorithm(row_list)
    if not row_list or not summary:
        return "No result rows were available to summarize."

    fastest = min(summary, key=lambda algorithm: summary[algorithm]["mean_runtime_ms"])
    lowest_cost = min(summary, key=lambda algorithm: summary[algorithm]["mean_path_cost"])
    graph_count = len({str(row["graph_id"]) for row in row_list})
    hs_error = _mean_harmony_error(row_list)

    lines = [
        "",
        "Result perspective:",
        f"- Compared {len(summary)} algorithms across {graph_count} graph instance(s) and {len(row_list)} total runs.",
        f"- Fastest average runtime: {fastest} ({summary[fastest]['mean_runtime_ms']:.3f} ms).",
        f"- Lowest average path cost: {lowest_cost} ({summary[lowest_cost]['mean_path_cost']:.3f}).",
    ]
    if hs_error is not None:
        lines.append(f"- Harmony Search averaged {hs_error:.3f} cost units above Dijkstra on matching graphs.")
    lines.extend(
        [
            "- Dijkstra is the exact benchmark; matching its path cost means an algorithm found an optimal route.",
            "- Harmony Search is approximate, so its value is judged by how close it gets to Dijkstra and how much runtime it needs.",
        ]
    )
    return "\n".join(lines)


def _mean_harmony_error(rows: list[dict[str, object]]) -> float | None:
    dijkstra_cost: dict[str, float] = {}
    harmony_costs: dict[str, list[float]] = {}
    for row in rows:
        path_cost = row.get("path_cost")
        if path_cost in ("", None):
            continue
        graph_id = str(row["graph_id"])
        algorithm = str(row["algorithm"])
        cost = float(path_cost)
        if algorithm == "dijkstra":
            dijkstra_cost.setdefault(graph_id, cost)
        elif algorithm == "harmony_search":
            harmony_costs.setdefault(graph_id, []).append(cost)

    errors = []
    for graph_id, costs in harmony_costs.items():
        if graph_id in dijkstra_cost:
            errors.extend(cost - dijkstra_cost[graph_id] for cost in costs)
    return mean(errors) if errors else None


def _run_graph_trials(
    graph: WeightedGraph,
    graph_id: str,
    density: str,
    source: int,
    target: int,
    config: ExperimentConfig,
    graph_seed: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    exact_algorithms = (dijkstra, bellman_ford, astar)
    for algorithm in exact_algorithms:
        for _ in range(config.deterministic_repeats):
            result = algorithm(graph, source, target)
            rows.append(result_to_row(result, graph, graph_id, density, source, target))

    for trial in range(config.harmony_trials):
        result = harmony_search(
            graph,
            source,
            target,
            hmcr=config.hmcr,
            par=config.par,
            hms=config.hms,
            iterations=config.harmony_iterations,
            seed=graph_seed * 1000 + trial,
        )
        rows.append(result_to_row(result, graph, graph_id, density, source, target))
    return rows
