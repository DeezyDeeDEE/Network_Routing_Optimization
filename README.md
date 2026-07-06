# Routing Algorithm Comparison

CSC 2400 term project comparing routing algorithms on weighted network graphs.
The project evaluates Dijkstra, Bellman-Ford, A*, and Harmony Search to study
runtime, path quality, and the tradeoff between exact classical algorithms and
a nature-inspired metaheuristic.

## Team

- Aaron Werth
- Spencer Kirksey
- Derek Nelson
- Alan Tate



## Repository Structure

- `src/routing_project/`: graph utilities, algorithm implementations, experiment runner, and CLI.
- `tests/`: unit and smoke tests for graph generation, algorithms, and result writing.
- `results/raw/`: generated CSV experiment outputs.
- `results/charts/`: generated SVG charts for the report.
- `reports/`: checkpoint and project reports.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install -r requirements-dev.txt
```

If you do not create a virtual environment, run commands with `PYTHONPATH=src`.
On PowerShell:

```powershell
$env:PYTHONPATH = "src"
```

## Run Tests

Preferred:

```powershell
python -m pytest
```

Fallback using only the Python standard library:

```powershell
python -m unittest discover
```

## Run Experiments

Quick checkpoint run:

```powershell
python -m routing_project.cli run-small
```

Harmony Search parameter sweep:

```powershell
python -m routing_project.cli run-sweep
```

Larger checkpoint grid:

```powershell
python -m routing_project.cli run-checkpoint
```

Generate charts from the small run:

```powershell
python -m routing_project.cli make-charts
```

## Result Files

CSV outputs use these fields:

`algorithm`, `graph_id`, `nodes`, `edges`, `density`, `source`, `target`,
`path_cost`, `runtime_ms`, `success`, `seed`, `hmcr`, `par`, `hms`,
`iterations`.

The SVG chart outputs summarize mean runtime, mean path cost, and Harmony Search
cost difference relative to Dijkstra. These files can be inserted into the final
report or presentation.

## Current Status

Implemented and tested:

- Connected weighted graph generation.
- Dijkstra shortest path.
- Bellman-Ford shortest path and negative-cycle detection.
- A* with a pluggable heuristic.
- Harmony Search with configurable `HMCR`, `PAR`, `HMS`, iteration count, and seed.
- CSV result generation and dependency-free SVG chart generation.

