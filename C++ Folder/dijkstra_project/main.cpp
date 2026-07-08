#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <limits>
#include <algorithm>
#include <string>
#include <chrono>
#include <iomanip>
#include <cmath>

using namespace std;
using Clock = chrono::high_resolution_clock;

struct Edge {
    int to;
    int weight;
};

using Graph = unordered_map<int, vector<Edge>>;

struct DijkstraResult {
    unordered_map<int, int> distance;
    unordered_map<int, int> previous;
};

void printHeader() {
    cout << "=====================================================\n";
    cout << " CSC 2400 - Dijkstra's Algorithm Project\n";
    cout << " Student: Alan Tate\n";
    cout << " Dataset: Stanford SNAP as-Skitter\n";
    cout << "=====================================================\n\n";
}

void addUndirectedEdge(Graph& graph, int from, int to, int weight) {
    graph[from].push_back({to, weight});
    graph[to].push_back({from, weight});
}

Graph loadGraph(const string& filename, long long maxEdges, long long& edgeCount, int& minNode, int& maxNode) {
    ifstream file(filename);
    if (!file.is_open()) {
        throw runtime_error("Could not open file: " + filename + "\nMake sure as-skitter.txt is in the project folder and is unzipped.");
    }

    Graph graph;
    string line;
    edgeCount = 0;
    minNode = numeric_limits<int>::max();
    maxNode = numeric_limits<int>::min();

    while (getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;

        stringstream ss(line);
        int from, to;
        if (ss >> from >> to) {
            addUndirectedEdge(graph, from, to, 1);
            edgeCount++;
            minNode = min(minNode, min(from, to));
            maxNode = max(maxNode, max(from, to));
        }

        if (maxEdges > 0 && edgeCount >= maxEdges) break;
    }

    if (edgeCount == 0) {
        minNode = 0;
        maxNode = 0;
    }

    return graph;
}

DijkstraResult dijkstra(const Graph& graph, int source) {
    const int INF = numeric_limits<int>::max();
    unordered_map<int, int> distance;
    unordered_map<int, int> previous;
    distance.reserve(graph.size());
    previous.reserve(graph.size());

    for (const auto& item : graph) distance[item.first] = INF;

    if (distance.find(source) == distance.end()) {
        throw runtime_error("Source node was not found in the graph.");
    }

    distance[source] = 0;
    using QueueItem = pair<int, int>; // distance, node
    priority_queue<QueueItem, vector<QueueItem>, greater<QueueItem>> pq;
    pq.push({0, source});

    while (!pq.empty()) {
        int currentDistance = pq.top().first;
        int currentNode = pq.top().second;
        pq.pop();

        if (currentDistance > distance[currentNode]) continue;

        auto it = graph.find(currentNode);
        if (it == graph.end()) continue;

        for (const Edge& edge : it->second) {
            int newDistance = currentDistance + edge.weight;
            if (newDistance < distance[edge.to]) {
                distance[edge.to] = newDistance;
                previous[edge.to] = currentNode;
                pq.push({newDistance, edge.to});
            }
        }
    }

    return {distance, previous};
}

vector<int> buildPath(int source, int target, const unordered_map<int, int>& previous) {
    vector<int> path;
    int current = target;
    path.push_back(current);

    while (current != source) {
        auto it = previous.find(current);
        if (it == previous.end()) return {};
        current = it->second;
        path.push_back(current);
    }

    reverse(path.begin(), path.end());
    return path;
}

double secondsBetween(Clock::time_point start, Clock::time_point end) {
    return chrono::duration<double>(end - start).count();
}

string pathToString(const vector<int>& path, size_t limit = 25) {
    if (path.empty()) return "unreachable";

    stringstream out;
    if (path.size() <= limit) {
        for (size_t i = 0; i < path.size(); i++) {
            out << path[i];
            if (i + 1 < path.size()) out << " -> ";
        }
    } else {
        for (size_t i = 0; i < limit / 2; i++) out << path[i] << " -> ";
        out << "... -> ";
        for (size_t i = path.size() - limit / 2; i < path.size(); i++) {
            out << path[i];
            if (i + 1 < path.size()) out << " -> ";
        }
    }
    return out.str();
}

void writeResultsCSV(const string& filename, long long nodes, long long edges, double loadTime, double dijkstraTime, double totalTime, int source, int target, int distance, int pathLength) {
    ofstream file(filename);
    file << "algorithm,nodes,edges,load_time_seconds,algorithm_time_seconds,total_time_seconds,source,target,distance,path_length\n";
    file << "Dijkstra," << nodes << "," << edges << "," << fixed << setprecision(6)
         << loadTime << "," << dijkstraTime << "," << totalTime << ","
         << source << "," << target << "," << distance << "," << pathLength << "\n";
}

void writeRuntimeSVG(const string& filename, double loadTime, double dijkstraTime, double totalTime) {
    ofstream svg(filename);
    double maxVal = max(totalTime, max(loadTime, dijkstraTime));
    if (maxVal <= 0) maxVal = 1;

    int width = 760, height = 430;
    int left = 170, top = 55, barH = 48, gap = 35;
    int maxBarW = 500;

    vector<pair<string, double>> data = {
        {"Graph load", loadTime},
        {"Dijkstra", dijkstraTime},
        {"Total runtime", totalTime}
    };

    svg << "<svg xmlns='http://www.w3.org/2000/svg' width='" << width << "' height='" << height << "'>\n";
    svg << "<rect width='100%' height='100%' fill='white'/>\n";
    svg << "<text x='30' y='32' font-family='Arial' font-size='22' font-weight='bold'>Dijkstra Runtime Results</text>\n";
    svg << "<text x='30' y='55' font-family='Arial' font-size='13'>Stanford SNAP as-Skitter dataset</text>\n";

    for (size_t i = 0; i < data.size(); i++) {
        int y = top + 45 + i * (barH + gap);
        int barW = static_cast<int>((data[i].second / maxVal) * maxBarW);
        svg << "<text x='30' y='" << (y + 31) << "' font-family='Arial' font-size='15'>" << data[i].first << "</text>\n";
        svg << "<rect x='" << left << "' y='" << y << "' width='" << barW << "' height='" << barH << "' rx='6' ry='6' fill='#4f81bd'/>\n";
        svg << "<text x='" << (left + barW + 10) << "' y='" << (y + 31) << "' font-family='Arial' font-size='14'>" << fixed << setprecision(4) << data[i].second << " sec</text>\n";
    }

    svg << "<line x1='" << left << "' y1='350' x2='" << (left + maxBarW) << "' y2='350' stroke='black'/>\n";
    svg << "<text x='" << left << "' y='380' font-family='Arial' font-size='13'>0 sec</text>\n";
    svg << "<text x='" << (left + maxBarW - 70) << "' y='380' font-family='Arial' font-size='13'>" << fixed << setprecision(2) << maxVal << " sec</text>\n";
    svg << "</svg>\n";
}

void writePathSVG(const string& filename, int source, int target, int distance, int pathLength) {
    ofstream svg(filename);
    int width = 760, height = 360;
    int left = 210, top = 105, barH = 52, gap = 45, maxBarW = 450;
    int maxVal = max(1, max(distance, pathLength));

    vector<pair<string, int>> data = {
        {"Distance in edges", distance < 0 ? 0 : distance},
        {"Nodes in path", pathLength < 0 ? 0 : pathLength}
    };

    svg << "<svg xmlns='http://www.w3.org/2000/svg' width='" << width << "' height='" << height << "'>\n";
    svg << "<rect width='100%' height='100%' fill='white'/>\n";
    svg << "<text x='30' y='32' font-family='Arial' font-size='22' font-weight='bold'>Dijkstra Path Result</text>\n";
    svg << "<text x='30' y='56' font-family='Arial' font-size='13'>Path from node " << source << " to node " << target << "</text>\n";

    for (size_t i = 0; i < data.size(); i++) {
        int y = top + i * (barH + gap);
        int barW = static_cast<int>((static_cast<double>(data[i].second) / maxVal) * maxBarW);
        svg << "<text x='30' y='" << (y + 33) << "' font-family='Arial' font-size='15'>" << data[i].first << "</text>\n";
        svg << "<rect x='" << left << "' y='" << y << "' width='" << barW << "' height='" << barH << "' rx='6' ry='6' fill='#70ad47'/>\n";
        svg << "<text x='" << (left + barW + 10) << "' y='" << (y + 33) << "' font-family='Arial' font-size='14'>" << data[i].second << "</text>\n";
    }

    svg << "<line x1='" << left << "' y1='285' x2='" << (left + maxBarW) << "' y2='285' stroke='black'/>\n";
    svg << "<text x='" << left << "' y='315' font-family='Arial' font-size='13'>0</text>\n";
    svg << "<text x='" << (left + maxBarW - 20) << "' y='315' font-family='Arial' font-size='13'>" << maxVal << "</text>\n";
    svg << "</svg>\n";
}

int main(int argc, char* argv[]) {
    try {
        string filename = "as-skitter.txt";
        int source = 0;
        long long maxEdges = 100000;
        int targetOverride = -1;

        if (argc >= 2) filename = argv[1];
        if (argc >= 3) source = stoi(argv[2]);
        if (argc >= 4) maxEdges = stoll(argv[3]);
        if (argc >= 5) targetOverride = stoi(argv[4]);

        printHeader();

        cout << "Input Settings\n";
        cout << "--------------\n";
        cout << "File              : " << filename << endl;
        cout << "Source Node       : " << source << endl;
        cout << "Max Edges Loaded  : " << (maxEdges == 0 ? string("ALL") : to_string(maxEdges)) << "\n\n";

        cout << "Loading graph...\n";
        auto totalStart = Clock::now();
        auto loadStart = Clock::now();

        long long edgeCount = 0;
        int minNode = 0, maxNode = 0;
        Graph graph = loadGraph(filename, maxEdges, edgeCount, minNode, maxNode);

        auto loadEnd = Clock::now();
        double loadTime = secondsBetween(loadStart, loadEnd);

        int target = (targetOverride >= 0) ? targetOverride : maxNode;

        cout << "Complete!\n\n";
        cout << "Dataset Statistics\n";
        cout << "------------------\n";
        cout << "Nodes Loaded      : " << graph.size() << endl;
        cout << "Edges Loaded      : " << edgeCount << endl;
        cout << "First Node ID     : " << minNode << endl;
        cout << "Last Node ID      : " << maxNode << endl;
        cout << fixed << setprecision(4);
        cout << "Graph Load Time   : " << loadTime << " seconds\n\n";

        cout << "Algorithm Information\n";
        cout << "---------------------\n";
        cout << "Algorithm           : Dijkstra's Algorithm\n";
        cout << "Graph Representation: Adjacency List\n";
        cout << "Edge Weights        : 1 (Unweighted Dataset)\n\n";

        cout << "Running Dijkstra's algorithm...\n";
        auto dijkstraStart = Clock::now();
        DijkstraResult result = dijkstra(graph, source);
        auto dijkstraEnd = Clock::now();
        double dijkstraTime = secondsBetween(dijkstraStart, dijkstraEnd);
        double totalTime = secondsBetween(totalStart, dijkstraEnd);
        cout << "Complete!\n\n";

        cout << "Performance Results\n";
        cout << "-------------------\n";
        cout << "Dijkstra Time     : " << dijkstraTime << " seconds\n";
        cout << "Total Runtime     : " << totalTime << " seconds\n\n";

        cout << "Complexity Analysis\n";
        cout << "-------------------\n";
        cout << "Time Complexity   : O((V + E) log V)\n";
        cout << "Space Complexity  : O(V + E)\n\n";

        cout << "Path From First/Source Node To Last Node\n";
        cout << "----------------------------------------\n";
        int targetDistance = -1;
        int targetPathLength = -1;

        if (!result.distance.count(target) || result.distance[target] == numeric_limits<int>::max()) {
            cout << "Source: " << source << "\n";
            cout << "Target: " << target << "\n";
            cout << "Path  : unreachable\n\n";
        } else {
            vector<int> targetPath = buildPath(source, target, result.previous);
            targetDistance = result.distance[target];
            targetPathLength = static_cast<int>(targetPath.size());

            cout << "Source   : " << source << "\n";
            cout << "Target   : " << target << "\n";
            cout << "Distance : " << targetDistance << " edge(s)\n";
            cout << "Path Len : " << targetPathLength << " node(s)\n";
            cout << "Path     : " << pathToString(targetPath) << "\n\n";
        }

        vector<int> targets = {10, 100, 500, 1000, 5000, 10000};
        cout << "Sample Shortest Path Results From Node " << source << "\n";
        cout << "----------------------------------------\n";

        for (int sampleTarget : targets) {
            cout << "Node " << left << setw(7) << sampleTarget << " Distance: ";
            if (!result.distance.count(sampleTarget) || result.distance[sampleTarget] == numeric_limits<int>::max()) {
                cout << "unreachable\n";
            } else {
                cout << result.distance[sampleTarget] << " edge(s)";
                vector<int> path = buildPath(source, sampleTarget, result.previous);
                if (!path.empty() && path.size() <= 15) {
                    cout << " | Path: " << pathToString(path, 15);
                }
                cout << endl;
            }
        }

        writeResultsCSV("results.csv", graph.size(), edgeCount, loadTime, dijkstraTime, totalTime, source, target, targetDistance, targetPathLength);
        writeRuntimeSVG("runtime_graph.svg", loadTime, dijkstraTime, totalTime);
        writePathSVG("path_length_graph.svg", source, target, targetDistance, targetPathLength);

        cout << "\nOutput Files Created\n";
        cout << "--------------------\n";
        cout << "results.csv\n";
        cout << "runtime_graph.svg\n";
        cout << "path_length_graph.svg\n\n";

        cout << "Project Notes\n";
        cout << "-------------\n";
        cout << "Dataset: Stanford SNAP as-Skitter\n";
        cout << "Nodes Processed: " << graph.size() << "\n";
        cout << "Edges Processed: " << edgeCount << "\n";
        cout << "Graph stored using an adjacency list.\n";
        cout << "An adjacency matrix was not used because it would require too much memory.\n";
        cout << "Every edge is treated as weight 1 because the dataset is unweighted.\n\n";

        cout << "=====================================================\n";
        cout << " Project Completed Successfully\n";
        cout << "=====================================================\n";
        cout << "Dataset Parsed Successfully\n";
        cout << "Adjacency List Created\n";
        cout << "Dijkstra's Algorithm Executed\n";
        cout << "Shortest Paths Computed\n";
        cout << "Performance Statistics Generated\n";
        cout << "Graph Files Generated\n";
        cout << "=====================================================\n";

    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}
