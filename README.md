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
- `/Code/Python Folder/`: code that contains the implementations of Derek and Aaron
- `/Code/C++ Folder/`: Code that contains the implementation of the algorithms from Alan
- `/Reports/`: Contains the reports of the implementations of Alan and Derek's Code
- `/Graphs/`: Contains the graphs of Aaron's, Alan's, and Derek's implementations.

# How To Run Code For Each Implementation
## Derek Implementation
### Setup
- Navigate to `/Code/Python/Derek Implementation/`


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

## Analysis Notebook

`analysis.ipynb` walks through the whole study in 19 documented code cells:
each algorithm in turn, the scaling experiment, the real SNAP networks, memory
and basic-operation counts, and the Harmony Search parameter sweep. It is
committed **with all outputs saved**, so GitHub renders the tables and the six
figures without anyone running it.

```powershell
python -m pip install -r requirements-dev.txt
jupyter notebook analysis.ipynb
```

## Interactive GUI

The fastest way to see the project work is the built-in web GUI:

```powershell
python -m routing_project.cli gui
```

This starts a local server (default <http://127.0.0.1:8000>) and opens a browser.
From there you can pick an experiment, adjust its parameters, press **Run**, and
watch results stream in live: a progress bar, a running log, stat tiles, and four
charts (runtime, path cost, Harmony Search gap above optimal, peak memory) that
redraw as each run finishes. When the experiment ends, the report-quality SVG
charts are generated and shown at the bottom of the page.

Options: `--port 0` picks a free port, `--host 0.0.0.0` exposes it on the
network, `--no-browser` skips opening a browser.

The GUI uses only the Python standard library (`http.server` plus server-sent
events), so it adds no dependencies. Only one experiment runs at a time — these
measurements are wall-clock timings, and two experiments sharing the CPU would
contaminate each other's results.

## Run Experiments

Quick checkpoint run:

```powershell
python -m routing_project.cli run-small
```

Harmony Search parameter sweep:

```powershell
python -m routing_project.cli run-sweep
```

The default sweep tests all HMCR/PAR/HMS combinations at 500 nodes with 3
trials and 100 iterations per trial. For a larger final-analysis run:

```powershell
python -m routing_project.cli run-sweep --trials 10 --iterations 250
```

Larger checkpoint grid:

```powershell
python -m routing_project.cli run-checkpoint
```


```powershell
python -m routing_project.cli list-datasets
python -m routing_project.cli run-real
python -m routing_project.cli run-real --datasets facebook oregon1 --sample 5000
```

Files download once into `data/` and are cached. Two modelling decisions matter
for the report:


## Charts

```powershell
python -m routing_project.cli make-charts --input results/raw/checkpoint_experiment.csv --output-dir results/charts
python -m routing_project.cli make-charts --input results/raw/real_experiment.csv --output-dir results/charts/real
```
## Aaron Implementation
- Navigate to `/Code/Python/Aaron Implementation/`
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
- Navigate to `/Code/C++ Code/`
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
