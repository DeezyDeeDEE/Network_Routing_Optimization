# Network_Routing_Optimization
The purpose of this project is compare algorithms on weighted graphs with 4 different algorithms.
This project will use Dijkstra's, Bellman Ford, A*, and Harmoncy search as the comparisons. We will also
be comparing the efficiency between C++ algorithms and Python algorithms as well.

## Team
- Spencer Kirksey(https://github.com/DeezyDeeDEE) - Organizer
- Aaron Werth(https://github.com/awwerth42) - Python Collaborator
- Derek Nelson(https://github.com/Nex-png) - Python Collaborator
- Alan Tate(https://github.com/Reaper51322) - C++ Collaborator

## Structure
- `/Python Folder/Aaron Files/`: Code from Aaron and his graphs, results, and his implementation of the algorithm's
- `/Python Folder/Derek Code/`: Code from Derek and his graphs, results, tests, and algorithm implementations
- `/C++ Folder/`: Contains seperate folders for Alan's algorithms
- `/C++ Folder/A search/`: Contains files from A search implementation including code, graphs, reports, and tests
- `/C++ Folder/Harmoncy search/`:Contains Harmony search implementation files including code, graphs, reports, and tests
- `/C++ Folder/bellman_ford/`: Contains Bellman-Ford implementation files including code, graphs, reports, and tests
- `/C++ Folder/dijkstra_project/`: Contains Dijkstra'simplementation files including code, graphs, reports, and tests

# How To Run Code For Each Implementation
## Derek Implementation
### Setup
- Navigate to `/Python Folder/Derek Code/`

Run code for setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install -r requirements-dev.txt
```

If you have not created a python environment, run the commands with `PYTHONPATH=src`.
On PowerShell:
```powershell
$env:PYTHONPATH = "src"
```
Preferred:

```powershell
python -m pytest
```

Fallback using only the Python standard library:

```powershell
python -m unittest discover
```

### Run Experiments

Quick checkpoint run:

```powershell
python -m routing_project.cli run-small
```

Harmony Search parameter sweep:

```powershell
python -m routing_project.cli run-sweep
```

- The default sweep tests all HMCR/PAR/HMS combinations at 500 nodes with 3
trials and 100 iterations per trial. For a larger final-analysis run:

```powershell
python -m routing_project.cli run-sweep --trials 10 --iterations 250
```

Larger checkpoint grid:

```powershell
python -m routing_project.cli run-checkpoint
```

- Generate charts from the small run:

```powershell
python -m routing_project.cli make-charts
```

This writes SVG chart files and `results/charts/results_summary.md`, which
summarizes the fastest algorithm, lowest path-cost algorithm, Harmony Search's
average gap from Dijkstra, and the main interpretation points for the report.

### Result Files

- CSV outputs use these fields:

`algorithm`, `graph_id`, `nodes`, `edges`, `density`, `source`, `target`,
`path_cost`, `runtime_ms`, `success`, `seed`, `hmcr`, `par`, `hms`,
`iterations`.

The SVG chart outputs summarize mean runtime, mean path cost, and Harmony Search
cost difference relative to Dijkstra. These files can be inserted into the final
report or presentation.

## Aaron Implementation
- Navigate to `/Python Folder/Aaron Files/`
To run, simply input the following
```powershell
./mainscript.sh
```
To put the results in a file and graph them, input the following
```powershell
./mainscript.sh
./mainscript.sh > results.csv
python3 graph.py
```
## Alan Implementation
- Navigate to `/C++ Folder/`
### Dijkstra's Algorithm
- Navigate to `/C++ Folder/dijkstra_project/`
The file must be unzipped first. Use `as-skitter.txt`, not `as-skitter.txt.gz`.

#### Compile in VS Code terminal

```powershell
g++ main.cpp -o dijkstra -std=c++17
```

Or use Make:

```powershell
make
```

#### Run a smaller test

```powershell
.\dijkstra.exe as-skitter.txt 0 100000
```

#### Run the full dataset

```powershell
.\dijkstra.exe as-skitter.txt 0 0
```

#### Optional target node

By default, the program finds the path from the source node to the largest node ID loaded. You can also provide a target node manually:

```powershell
.\dijkstra.exe as-skitter.txt 0 0 1696415
```

#### Output files

The program creates:

- `results.csv`
- `runtime_graph.svg`
- `path_length_graph.svg`

### A* Search Algorithm
- Navigate to `/C++ Folder/A search/

Compile:
```powershell
g++ main.cpp -o astar -std=c++17 -O2
```

Run:
```powershell
.\astar.exe as-skitter.txt 0 0
```

This creates `results.csv`, `runtime_graph.svg`, and `path_length_graph.svg`.

### Bellman-Ford Algorithm
- Navigate to `/C++ Folder/bellman_ford/`
Compile:
```powershell
g++ main.cpp -o bellman_ford -std=c++17 -O2
```

Run:
```powershell
.\bellman_ford.exe as-skitter.txt 0 10000
```

This creates `results.csv`, `runtime_graph.svg`, and `path_length_graph.svg`.

### Harmony Search
- Navigate to `/C++ Folder/Harmoncy search/
Compile:
```powershell
g++ main.cpp -o harmony_search -std=c++17 -O2
```

Run:
```powershell
.\harmony_search.exe as-skitter.txt 0 100000 5000 50
```

Arguments: dataset source maxEdges iterations harmonyMemorySize.

This creates `results.csv`, `runtime_graph.svg`, and `path_length_graph.svg`.
