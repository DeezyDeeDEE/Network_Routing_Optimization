import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("results.csv")

# Extract the first two columns
num_nodes = df.iloc[:, 0]
time_seconds = df.iloc[:, 1]

# Create the figure
plt.figure(figsize=(10, 6))

# Plot the data in green
plt.plot(
    num_nodes,
    time_seconds,
    color="green",
    marker="o",
    linewidth=2,
    markersize=6,
    label="Dijkstra's Algorithm"
)

# Labels and title
plt.title("Dijkstra's Algorithm Runtime vs. Graph Size", fontsize=16)
plt.xlabel("Number of Nodes", fontsize=12)
plt.ylabel("Execution Time (Seconds)", fontsize=12)

# Add grid and legend
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Improve layout
plt.tight_layout()

# Save the graph
plt.savefig("dijkstra_runtime_graph.png", dpi=300)

# Display the graph
plt.show()
