CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra
TARGET = dijkstra

all: $(TARGET)

$(TARGET): main.cpp
	$(CXX) $(CXXFLAGS) main.cpp -o $(TARGET)

clean:
	rm -f $(TARGET) *.exe results.csv runtime_graph.svg path_length_graph.svg
