# Dijkstra's Algorithm C++ Project

This project runs Dijkstra's algorithm on the Stanford SNAP as-Skitter network dataset.

## Dataset

The as-Skitter dataset is an undirected and unweighted Internet Autonomous System network.

- Nodes: 1,696,415
- Edges: 11,095,298
- Format: `FromNodeId ToNodeId`

The file must be unzipped first. Use `as-skitter.txt`, not `as-skitter.txt.gz`.

## Compile in VS Code terminal

```powershell
g++ main.cpp -o dijkstra -std=c++17
```

Or use Make:

```powershell
make
```

## Run a smaller test

```powershell
.\dijkstra.exe as-skitter.txt 0 100000
```

## Run the full dataset

```powershell
.\dijkstra.exe as-skitter.txt 0 0
```

## Optional target node

By default, the program finds the path from the source node to the largest node ID loaded. You can also provide a target node manually:

```powershell
.\dijkstra.exe as-skitter.txt 0 0 1696415
```

## Output files

The program creates:

- `results.csv`
- `runtime_graph.svg`
- `path_length_graph.svg`

## Complexity

Using a priority queue, Dijkstra's algorithm has:

- Time complexity: `O((V + E) log V)`
- Space complexity: `O(V + E)`
